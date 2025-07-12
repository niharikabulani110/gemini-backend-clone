from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, user, chatroom, message, subscription
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

# Route includes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(chatroom.router, prefix="/chatroom", tags=["Chatroom"])
app.include_router(message.router, prefix="/chatroom", tags=["Message"])
app.include_router(subscription.router, prefix="/subscription", tags=["Subscription"])

@app.get("/")
def root():
    return {"message": "Gemini Backend API is live"}
