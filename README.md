# 🚀 Ascend AI

**AI-powered Resume Analyzer & Job Optimization Platform**

Ascend AI is an AI-powered platform designed to help job seekers optimize their resumes for specific job roles. Upload your resume, provide a Job Description, and receive detailed AI-generated insights, ATS optimization suggestions, and actionable recommendations to improve your chances of landing interviews.

> **🚧 Status:** Active Development

---

# ✨ Features

## ✅ Authentication

* Secure JWT Authentication
* HTTP-only Cookie-based Sessions
* Email Verification
* Password Reset via Email
* Session Management

## 🚧 Resume Management *(In Progress)*

* Upload PDF resumes
* Resume parsing and text extraction
* Resume history

## 🚧 AI Resume Analysis *(Planned)*

* ATS compatibility analysis
* Resume scoring
* Skills gap identification
* Keyword optimization
* Section-wise feedback
* Personalized AI suggestions

## 🚧 Job Description Matching *(Planned)*

* Upload or paste a Job Description
* Resume vs JD comparison
* Match score generation
* Missing skills detection
* Tailored recommendations

## 🚧 AI Chat *(Planned)*

* Chat with your resume
* Ask resume-specific questions
* AI-powered resume improvement suggestions
* Career guidance based on your profile

---

# 🏗️ Architecture

```text
                   +----------------------+
                   |    Next.js Frontend  |
                   +----------+-----------+
                              |
                              |
                              v
                   +----------------------+
                   |      FastAPI API     |
                   +----------+-----------+
                              |
          +-------------------+-------------------+
          |                                       |
          |                                       |
          v                                       v
     PostgreSQL                           Object Storage
                                                  |
                                                  |
                                                  v
                                           AI Processing
                                                  |
                                                  |
                                                  v
                                        Large Language Model
```

---

# 🛠 Tech Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Shadcn UI

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication
* Pydantic
* Bcrypt

### AI

* Large Language Models
* Prompt Engineering

### DevOps

* Docker

---

# 📂 Repository Structure

```text
frontend/
backend/
```

---

# 🚀 Getting Started

## Clone the Repository

```bash
git clone https://github.com/yourusername/ascend-ai.git

cd ascend-ai
```

---

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=

SECRET_KEY=

ALGORITHM=

SMTP_HOST=

SMTP_PORT=

SMTP_USERNAME=

SMTP_PASSWORD=
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Create `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run:

```bash
npm run dev
```

---

# 📅 Roadmap

* [x] Authentication System
* [ ] Resume Upload
* [ ] Resume Parsing
* [ ] Resume Dashboard
* [ ] AI Resume Analysis
* [ ] ATS Score Generation
* [ ] Job Description Matching
* [ ] AI Chat Assistant
* [ ] Resume Version History
* [ ] Export Optimized Resume
* [ ] Docker Deployment
* [ ] CI/CD Pipeline

---

# 🤝 Contributing

Contributions, suggestions, and feedback are always welcome.

Feel free to open an issue or submit a pull request.

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub. It helps the project reach more developers and keeps me motivated to continue building it.

---

# 📄 License

This project is licensed under the MIT License.

---

Built with ❤️ using **Next.js**, **FastAPI**, and AI.
