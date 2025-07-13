from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth, user, chatroom, message, subscription, webhook
from app.core.config import settings
from app.database import create_tables

app = FastAPI(title="Gemini Style Backend System")

# Initialize database tables
@app.on_event("startup")
async def startup_event():
    create_tables()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Route includes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(chatroom.router, prefix="/chatroom", tags=["Chatroom"])
app.include_router(message.router, prefix="/chatroom", tags=["Message"])
app.include_router(subscription.router, prefix="/subscription", tags=["Subscription"])
app.include_router(webhook.router, tags=["Webhook"])

@app.get("/")
def root():
    return {"message": "Gemini Backend API is live"}
