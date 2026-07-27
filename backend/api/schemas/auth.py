"""
Pydantic schemas for authentication endpoints.

Schemas define the shape of request and response data.
They validate input automatically and generate API documentation.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRegister(BaseModel):
    """Schema for user registration request."""
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema for user data response."""
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
