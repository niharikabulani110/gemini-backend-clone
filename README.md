# Gemini Style Backend System

A comprehensive backend system that enables user-specific chatrooms, OTP-based login, Gemini API-powered AI conversations, and subscription handling via Stripe.

## 🚀 Features

- **User Authentication**: OTP-based login system with mobile number verification
- **Chatroom Management**: Create and manage multiple chatrooms with AI conversations
- **Gemini AI Integration**: Powered by Google Gemini API with async message processing
- **Subscription System**: Stripe integration with Basic (free) and Pro (paid) tiers
- **Rate Limiting**: Daily message limits for Basic tier users
- **Caching**: Redis-based caching for improved performance
- **Message Queue**: Celery-based async processing for AI responses

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   PostgreSQL    │    │     Redis       │
│   (Port 8000)   │◄──►│   (Port 5433)   │    │   (Port 6380)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Celery Worker │    │   Gemini API    │    │   Stripe API    │
│   (Async Tasks) │    │   (External)    │    │   (External)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 14 with SQLAlchemy ORM
- **Cache**: Redis 7.0
- **Message Queue**: Celery with Redis broker
- **Authentication**: JWT tokens with bcrypt password hashing
- **Payments**: Stripe (sandbox mode)
- **AI**: Google Gemini API
- **Containerization**: Docker & Docker Compose

### Project Structure

```
app/
├── api/                    # API route handlers
│   ├── auth.py            # Authentication endpoints
│   ├── user.py            # User management
│   ├── chatroom.py        # Chatroom operations
│   ├── message.py         # Message handling
│   ├── subscription.py    # Stripe subscriptions
│   └── webhook.py         # Stripe webhooks
├── cache/                 # Redis caching layer
│   └── redis_cache.py     # Chatroom caching
├── core/                  # Core utilities
│   ├── config.py          # Environment configuration
│   └── security.py        # JWT & password utilities
├── models/                # Database models
│   ├── user.py            # User model
│   ├── chatroom.py        # Chatroom model
│   ├── message.py         # Message model
│   └── subscription.py    # Subscription models
├── schemas/               # Pydantic schemas
│   ├── auth.py            # Auth request/response schemas
│   ├── user.py            # User schemas
│   ├── chatroom.py        # Chatroom schemas
│   ├── message.py         # Message schemas
│   └── subscription.py    # Subscription schemas
├── services/              # Business logic
│   ├── auth_service.py    # Authentication logic
│   ├── chatroom_service.py # Chatroom operations
│   ├── gemini_service.py  # Gemini API integration
│   ├── stripe_service.py  # Stripe integration
│   └── rate_limit_service.py # Rate limiting
└── workers/               # Celery tasks
    └── tasks.py           # Async task definitions
```

## 🔄 Queue System Explanation

### Why Celery?

The system uses Celery for asynchronous message processing to:

1. **Improve User Experience**: Users get immediate response while AI processing happens in background
2. **Handle API Rate Limits**: Gemini API has rate limits that async processing helps manage
3. **Scalability**: Multiple workers can process messages concurrently
4. **Reliability**: Failed tasks can be retried automatically

### Message Flow

```
1. User sends message → FastAPI endpoint
2. Message saved to database → Immediate response to user
3. Celery task queued → Redis broker
4. Celery worker picks up task → Calls Gemini API
5. AI response received → Saved to database
6. User can fetch updated chatroom → See AI response
```

### Celery Configuration

- **Broker**: Redis (for task queue)
- **Result Backend**: Redis (for task results)
- **Concurrency**: Configurable worker processes
- **Task Routing**: All AI tasks go to dedicated queue
- **Retry Logic**: Failed API calls retry with exponential backoff

## 🤖 Gemini API Integration Overview

### Integration Details

- **Model**: Gemini 1.5 Flash (latest stable)
- **Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- **Authentication**: API key via query parameter
- **Request Format**: JSON with content parts
- **Response Processing**: Extracts text from candidates

### Error Handling

- **API Errors**: Graceful handling of 401, 404, 429, 500 errors
- **Timeout**: 30-second timeout for API calls
- **Fallback**: Returns error message if API fails
- **Logging**: Detailed error logging for debugging

### Rate Limiting

- **Basic Users**: 5 messages per day
- **Pro Users**: Unlimited messages
- **API Level**: Respects Gemini API rate limits
- **Queue Management**: Tasks queued when limits exceeded

## 🎯 Design Decisions & Assumptions

### Authentication System

**Decision**: OTP + Password hybrid system
- **Why**: Combines security of OTP with convenience of password
- **Assumption**: OTP delivery is mocked (no SMS integration)
- **Security**: JWT tokens with 7-day expiration

### Database Design

**Decision**: Separate tables for users, chatrooms, messages, subscriptions
- **Why**: Normalized design for scalability
- **Assumption**: Users can have multiple chatrooms
- **Indexing**: Mobile number, user_id, chatroom_id indexed

### Caching Strategy

**Decision**: Redis caching for chatroom lists
- **Why**: Chatrooms don't change frequently, high read volume
- **TTL**: 5 minutes (balance between performance and freshness)
- **Invalidation**: Cache cleared when new chatroom created

### Subscription Model

**Decision**: Basic (free) vs Pro (paid) tiers
- **Basic**: 5 messages/day, limited features
- **Pro**: Unlimited messages, all features
- **Assumption**: Stripe handles payment processing
- **Webhook**: Real-time subscription status updates

### Message Processing

**Decision**: Asynchronous processing with immediate response
- **Why**: Better UX, handles API delays gracefully
- **Trade-off**: Users need to poll for AI responses
- **Alternative**: WebSocket for real-time updates (future enhancement)

## 🛠️ Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Git

### 1. Clone Repository

```bash
git clone <repository-url>
cd gemini-backend-clone
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

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

### 3. Running with Docker (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Manual Setup (Alternative)

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

## 🧪 Testing with Postman

### Quick Setup

1. **Import Collection**: Import `Gemini_Backend_API.postman_collection.json`
2. **Import Environment**: Import `Gemini_Backend_Environment.postman_environment.json`
3. **Select Environment**: Choose "Gemini Backend - Local" from dropdown
4. **Start Backend**: Ensure Docker containers are running

### Testing Workflow

#### 1. Authentication Flow
```bash
# 1. Signup
POST {{base_url}}/auth/signup
{
    "mobile_number": "+1234567890",
    "password": "testpassword123"
}

# 2. Send OTP
POST {{base_url}}/auth/send-otp
{
    "mobile_number": "+1234567890"
}

# 3. Verify OTP (JWT token auto-extracted)
POST {{base_url}}/auth/verify-otp
{
    "mobile_number": "+1234567890",
    "otp": "123456"
}
```

#### 2. Chatroom Testing
```bash
# 1. Create Chatroom
POST {{base_url}}/chatroom/
Authorization: Bearer {{access_token}}
{
    "name": "My AI Assistant"
}

# 2. List Chatrooms
GET {{base_url}}/chatroom/
Authorization: Bearer {{access_token}}

# 3. Get Chatroom Details
GET {{base_url}}/chatroom/{{chatroom_id}}
Authorization: Bearer {{access_token}}
```

#### 3. Message Testing
```bash
# Send Message (async response)
POST {{base_url}}/chatroom/{{chatroom_id}}/message
Authorization: Bearer {{access_token}}
{
    "content": "Hello, can you help me with Python programming?"
}
```

#### 4. Subscription Testing
```bash
# Check Status
GET {{base_url}}/subscription/status
Authorization: Bearer {{access_token}}

# Start Pro Subscription
POST {{base_url}}/subscription/pro
Authorization: Bearer {{access_token}}
```

### Automated Features

- **JWT Auto-Extraction**: Token automatically saved from OTP verification
- **Built-in Tests**: Each request includes validation tests
- **Environment Variables**: Easy configuration management

## 📊 API Endpoints

### Authentication
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/auth/signup` | POST | ❌ | Register new user |
| `/auth/send-otp` | POST | ❌ | Send OTP to mobile |
| `/auth/verify-otp` | POST | ❌ | Verify OTP & get JWT |
| `/auth/forgot-password` | POST | ❌ | Send reset OTP |
| `/auth/reset-password` | POST | ❌ | Reset password with OTP |
| `/auth/change-password` | POST | ✅ | Change password |

### User Management
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/user/me` | GET | ✅ | Get user profile |
| `/user/usage` | GET | ✅ | Get usage statistics |

### Chatrooms
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/chatroom/` | POST | ✅ | Create chatroom |
| `/chatroom/` | GET | ✅ | List chatrooms (cached) |
| `/chatroom/{id}` | GET | ✅ | Get chatroom details |

### Messages
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/chatroom/{id}/message` | POST | ✅ | Send message (async) |

### Subscriptions
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/subscription/pro` | POST | ✅ | Start Pro subscription |
| `/subscription/status` | GET | ✅ | Check subscription |

### Webhooks
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/webhook/stripe` | POST | ❌ | Stripe webhook handler |

## 🚀 Deployment Instructions

### Production Deployment

#### 1. Environment Variables
```env
# Production settings
DATABASE_URL=postgresql://user:pass@prod-db:5432/gemini
REDIS_URL=redis://prod-redis:6379
JWT_SECRET=very-long-random-secret-key
STRIPE_SECRET_KEY=sk_live_your_live_key
GEMINI_API_KEY=your_production_gemini_key
```

#### 2. Docker Production
```bash
# Build production image
docker build -t gemini-backend:prod .

# Run with production compose
docker-compose -f docker-compose.prod.yml up -d
```

#### 3. Cloud Deployment Options

**AWS ECS/Fargate**:
```bash
# Deploy to ECS
aws ecs create-service --cluster gemini-cluster --service-name gemini-backend
```

**Google Cloud Run**:
```bash
# Deploy to Cloud Run
gcloud run deploy gemini-backend --source .
```

**Heroku**:
```bash
# Deploy to Heroku
heroku create gemini-backend
git push heroku main
```

#### 4. Security Considerations

- **HTTPS**: Always use HTTPS in production
- **Secrets**: Use environment variables for all secrets
- **Rate Limiting**: Implement API-level rate limiting
- **CORS**: Configure CORS for your frontend domain
- **Database**: Use connection pooling in production

## 🔧 Development

### Adding New Features

1. **Create Models**: Add database models in `app/models/`
2. **Add Schemas**: Create Pydantic schemas in `app/schemas/`
3. **Implement Services**: Add business logic in `app/services/`
4. **Create API Endpoints**: Add routes in `app/api/`
5. **Add Tests**: Create tests for new functionality

### Code Style

- **Python**: Follow PEP 8 guidelines
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Add docstrings for all public functions
- **Error Handling**: Use proper exception handling

## 🐛 Troubleshooting

### Common Issues

1. **Connection Refused**: Check if all Docker containers are running
2. **JWT Token Issues**: Verify JWT_SECRET is set correctly
3. **Gemini API Errors**: Check API key and rate limits
4. **Celery Worker Issues**: Check Redis connection and worker logs
5. **Database Connection**: Verify DATABASE_URL and PostgreSQL status

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs app
docker-compose logs celery
docker-compose logs db
docker-compose logs redis

# Follow logs in real-time
docker-compose logs -f
```

## 📈 Performance Considerations

### Caching Strategy
- **Chatroom Lists**: 5-minute TTL in Redis
- **User Data**: Consider caching frequently accessed user data
- **API Responses**: Cache Gemini responses for similar queries

### Database Optimization
- **Indexes**: Ensure proper indexing on frequently queried columns
- **Connection Pooling**: Use connection pooling in production
- **Query Optimization**: Monitor slow queries and optimize

### Scalability
- **Horizontal Scaling**: Multiple Celery workers
- **Load Balancing**: Use load balancer for multiple app instances
- **Database Sharding**: Consider sharding for large-scale deployments

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Happy coding! 🚀** 