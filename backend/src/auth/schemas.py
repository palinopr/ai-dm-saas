"""Authentication schemas for request/response validation."""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration request."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    full_name: str | None = Field(None, max_length=255)


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""

    sub: str
    exp: datetime


class UserResponse(BaseModel):
    """Schema for user response."""

    id: str
    email: EmailStr
    full_name: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
