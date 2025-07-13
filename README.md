# Gemini Style Backend System

A comprehensive backend system that enables user-specific chatrooms, OTP-based login, Gemini API-powered AI conversations, and subscription handling via Stripe.

## Features

- **User Authentication**: OTP-based login system with mobile number verification
- **Chatroom Management**: Create and manage multiple chatrooms with AI conversations
- **Gemini AI Integration**: Powered by Google Gemini API with async message processing
- **Subscription System**: Stripe integration with Basic (free) and Pro (paid) tiers
- **Rate Limiting**: Daily message limits for Basic tier users
- **Caching**: Redis-based caching for improved performance
- **Message Queue**: Celery-based async processing for AI responses

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Message Queue**: Celery with Redis broker
- **Authentication**: JWT tokens
- **Payments**: Stripe
- **AI**: Google Gemini API
- **Containerization**: Docker & Docker Compose

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/gemini

# Redis
REDIS_URL=redis://redis:6379

# Celery
CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# Stripe (sandbox mode)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret_here

# Gemini
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### 3. Manual Setup (Alternative)

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis
redis-server

# Start PostgreSQL
# (Install and configure PostgreSQL)

# Start Celery worker
celery -A app.workers.tasks worker --loglevel=info

# Start FastAPI server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/send-otp` - Send OTP to mobile number
- `POST /auth/verify-otp` - Verify OTP and get JWT token
- `POST /auth/forgot-password` - Send OTP for password reset
- `POST /auth/change-password` - Change password (requires auth)
- `POST /auth/reset-password` - Reset password with OTP

### User Management
- `GET /user/me` - Get current user profile
- `GET /user/usage` - Get usage statistics

### Chatrooms
- `POST /chatroom/` - Create new chatroom
- `GET /chatroom/` - List user's chatrooms
- `GET /chatroom/{id}` - Get specific chatroom details

### Messages
- `POST /chatroom/{id}/message` - Send message to chatroom

### Subscriptions
- `POST /subscription/pro` - Start Pro subscription
- `GET /subscription/status` - Check subscription status

### Webhooks
- `POST /webhook/stripe` - Stripe webhook handler

## Rate Limiting

- **Basic Tier**: 5 messages per day
- **Pro Tier**: Unlimited messages

## Caching

- Chatroom lists are cached in Redis with 5-minute TTL
- Cache is invalidated when new chatrooms are created

## Development

### Project Structure
```
app/
├── api/           # API routes
├── cache/         # Redis caching
├── core/          # Core utilities
├── models/        # Database models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
└── workers/       # Celery tasks
```

### Adding New Features

1. Create models in `app/models/`
2. Add schemas in `app/schemas/`
3. Implement business logic in `app/services/`
4. Create API endpoints in `app/api/`
5. Add tests as needed

## Testing

```bash
# Run tests (when implemented)
pytest

# Test specific endpoint
curl -X POST "http://localhost:8000/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"mobile_number": "+1234567890"}'
```

## Production Deployment

1. Change JWT secret to a secure random string
2. Use production Stripe keys
3. Configure proper CORS origins
4. Set up proper database backups
5. Configure monitoring and logging
6. Use HTTPS in production

## License

MIT License
