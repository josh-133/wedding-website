from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    event_date = Column(Date, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    rsvps = relationship("RSVP", back_populates="event")


class RSVP(Base):
    __tablename__ = "rsvps"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String(200), nullable=False)  # Primary contact name
    email = Column(String(254), nullable=False)
    attending = Column(Boolean, nullable=False)
    guest_count = Column(Integer, nullable=False, default=1)  # Total number of guests (including primary)
    submitted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship("Event", back_populates="rsvps")
    guests = relationship("Guest", back_populates="rsvp", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("event_id", "email", name="unique_rsvp_per_event"),
    )


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    rsvp_id = Column(Integer, ForeignKey("rsvps.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    dietary_requirements = Column(String(500), nullable=True)
    is_primary = Column(Boolean, default=False)  # True for the primary contact

    rsvp = relationship("RSVP", back_populates="guests")
