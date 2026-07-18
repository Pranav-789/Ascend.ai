from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

services = {
    "authService": "http://localhost:8000"
}

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None, params=None):
    async with httpx.AsyncClient() as client:
        url = f"{service_url}{path}"
        response = await client.request(method, url, content=body, headers=headers, params=params)
        return response
    
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    if service not in services:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = services[service]
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    response = await forward_request(service_url, request.method, f"/{path}", body, headers, params=request.query_params)

    proxy_response = Response(status_code=response.status_code, content=response.content)
    
    # Forward headers to the client (especially Set-Cookie), ignoring hop-by-hop/encoding headers
    excluded_headers = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    for key, value in response.headers.multi_items():
        if key.lower() not in excluded_headers:
            proxy_response.headers.append(key, value)
            
    return proxy_response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
