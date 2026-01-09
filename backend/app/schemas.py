from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import date, datetime
from typing import Optional, List
import re


# Event schemas
class EventBase(BaseModel):
    name: str
    slug: str
    event_date: date
    description: Optional[str] = None


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# RSVP schemas
class RSVPCreate(BaseModel):
    event_slug: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    attending: bool

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        # Strip whitespace and validate
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        # Basic sanitization - remove any HTML-like tags
        v = re.sub(r'<[^>]*>', '', v)
        return v

    @field_validator('event_slug')
    @classmethod
    def validate_event_slug(cls, v: str) -> str:
        # Only allow alphanumeric and hyphens
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Invalid event slug format')
        return v


class RSVPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    attending: bool
    submitted_at: datetime
    event: EventResponse


class RSVPListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    attending: bool
    submitted_at: datetime
    event_name: str
    event_slug: str


# Admin schemas
class AdminLogin(BaseModel):
    password: str


class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StatsResponse(BaseModel):
    event_slug: str
    event_name: str
    total_responses: int
    attending: int
    not_attending: int


class RegistryResponse(BaseModel):
    registry_url: str
