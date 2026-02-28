from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator
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


# Guest schemas
class GuestCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    dietary_requirements: Optional[str] = Field(None, max_length=500)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        v = re.sub(r'<[^>]*>', '', v)
        return v

    @field_validator('dietary_requirements')
    @classmethod
    def validate_dietary(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        v = re.sub(r'<[^>]*>', '', v)
        return v


class GuestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    dietary_requirements: Optional[str]
    is_primary: bool


# RSVP schemas
class RSVPCreate(BaseModel):
    event_slug: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    postal_address: Optional[str] = Field(None, max_length=500)
    attending: bool
    dietary_requirements: Optional[str] = Field(None, max_length=500)  # Primary contact's dietary requirements
    guests: List[GuestCreate] = Field(default_factory=list, max_length=5)

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

    @field_validator('dietary_requirements')
    @classmethod
    def validate_dietary(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        v = re.sub(r'<[^>]*>', '', v)
        return v

    @field_validator('event_slug')
    @classmethod
    def validate_event_slug(cls, v: str) -> str:
        # Only allow alphanumeric and hyphens
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Invalid event slug format')
        return v

    @model_validator(mode='after')
    def validate_guest_count(self):
        # Include primary contact in count: max 5 total
        total_guests = 1 + len(self.guests)  # 1 for primary contact + additional guests
        if total_guests > 5:
            raise ValueError('Maximum of 5 guests allowed per RSVP (including yourself)')
        return self


class RSVPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    postal_address: Optional[str] = None
    attending: bool
    guest_count: int
    submitted_at: datetime
    event: EventResponse
    guests: List[GuestResponse]


class RSVPListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    postal_address: Optional[str] = None
    attending: bool
    guest_count: int
    submitted_at: datetime
    event_name: str
    event_slug: str
    guests: List[GuestResponse]


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
    total_guests_attending: int  # Total individual guests attending
    total_guests_not_attending: int  # Total individual guests not attending


class RegistryResponse(BaseModel):
    registry_url: str
