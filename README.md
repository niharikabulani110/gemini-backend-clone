# Gemini-Style Backend System (Kuvaka Tech Clone)

## 🚀 Tech Stack
- FastAPI
- PostgreSQL
- Redis + Celery
- Stripe (Sandbox)
- Google Gemini API

## ✅ Features
- OTP-based login via mobile
- JWT authentication
- Chatroom-based conversation system
- Async Gemini API using Celery
- Redis caching (chatroom listing)
- Stripe Pro subscription
- Rate-limiting support for free users

## ⚙️ Setup Instructions

### 1. Clone & Install
```bash
git clone https://github.com/your-username/gemini-backend.git
cd gemini-backend
cp .env.example .env
docker-compose up --build
