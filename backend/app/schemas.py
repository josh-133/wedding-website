from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List


# Event schemas
class EventBase(BaseModel):
    name: str
    slug: str
    event_date: date
    description: Optional[str] = None


class EventResponse(EventBase):
    id: int

    class Config:
        from_attributes = True


# RSVP schemas
class RSVPCreate(BaseModel):
    event_slug: str
    name: str
    email: EmailStr
    attending: bool


class RSVPResponse(BaseModel):
    id: int
    name: str
    email: str
    attending: bool
    submitted_at: datetime
    event: EventResponse

    class Config:
        from_attributes = True


class RSVPListResponse(BaseModel):
    id: int
    name: str
    email: str
    attending: bool
    submitted_at: datetime
    event_name: str
    event_slug: str

    class Config:
        from_attributes = True


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
