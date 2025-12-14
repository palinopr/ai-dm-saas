"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr


# Health check
class HealthResponse(BaseModel):
    """Health check response."""

    status: str
