from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class SubscriptionTier(str, enum.Enum):
    BASIC = "basic"
    PRO = "pro"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    otp = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    subscription = Column(Enum(SubscriptionTier), default=SubscriptionTier.BASIC)
    otp_generated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chatrooms = relationship("Chatroom", back_populates="user")
