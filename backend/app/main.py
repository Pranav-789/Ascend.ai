import time
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis.asyncio as redis
from typing import Optional
import os
from app.db.models.base import Base
from app.db.database import engine
from app.api.auth_router import authrouter
from app.api.user_router import userrouter

db = {}

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

@asynccontextmanager
async def lifespan(app: FastAPI):
    ## Before starting the application
    app.state.redis = redis.from_url(redis_url, decode_responses=True)
    db['redis'] = app.state.redis
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 

    ## Start seving request
    yield
    ## server is to be closed

    ## clean the application before closing
    await engine.dispose()
    await app.state.redis.aclose()

app = FastAPI(
    lifespan=lifespan,
    title="Ascend.ai",
    description='This ai application is a rag based system which provides user with a roadmap style report on the research papers of the topic they want to study',
    version='0.0.1-beta',
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RateLimiter:
    def __init__(self, route: str, window: int, max_reqs: int, method: str = 'ip'):
        self.route = route
        self.window = window
        self.max_reqs = max_reqs
        self.method = method

    async def __call__(self, request: Request, user_id: Optional[str]=None):
        redis_client = db.get('redis')

        if self.method == 'id':
            if not user_id:
                raise HTTPException(status_code=400, detail="Invalid request received") ## Not exposing why to protect the logic from attackers
            
            identifier = user_id
        else:
            identifier = request.client.host

        key = f"rate_limit:{self.route}:{identifier}"
        now = time.time() # current time
        cutoff = now-self.window # previous window

        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, "-inf", cutoff) # Removes the key value pairs before the cutoff time, like previous window and their precedings
            pipe.zadd(key, {str(now): now}) # adds the new key-val pairs
            pipe.zcard(key) # returns the number of vals per key (here total reqs per ip/user_id)
            pipe.expire(key, self.window) # expiry is applied on the key for cleanup, hopefully will not explode by redis memory
            results = await pipe.execute() # executes above written commands
            ## returns the reposne of every command the pipeline executes in a list format
        
        requests_count = results[2] 

        if requests_count > self.max_reqs:
            raise HTTPException(
                status_code=429,
                detail=f"Too many requests. Rate limit exceeded for {self.route}. Please try again after {self.window/60} minutes"
            )

        return True
    

auth_limiter = RateLimiter(route='/auth', window=60, max_reqs=5, method='ip')

app.include_router(authrouter)
app.include_router(userrouter)

@app.get('/')
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "message": f"{app.title} server is up and running on specified end point"
        }
    )
