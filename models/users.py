from pydantic import BaseModel, Field,  EmailStr
from typing import Optional, Any
from datetime import datetime, timezone


class User(BaseModel):
    name: str = Field(default=None, example="John Doe",
                      min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(default=None, example="Password",
                          min_length=3, max_length=128)
    userRole: str = Field(default="user")
    tier: int = Field(default=0)
    date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class LogUser(BaseModel):
    email: EmailStr
    password: str = Field(default=None, example="Password",
                          min_length=3, max_length=128)


class GoogleUser(BaseModel):
    name: str = Field(default=None, example="John Doe",
                      min_length=3, max_length=100)
    email: EmailStr
    sub: str
    picture: str = Field(default=None)
    userRole: str = Field(default="user")
    tier: int = Field(default=0)
    date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class LogGoogleUser(BaseModel):
    payload: object  # Using Any if the payload structure is not fixed or known
