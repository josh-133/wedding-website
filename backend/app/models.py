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
    name = Column(String(200), nullable=False)
    email = Column(String(254), nullable=False)
    attending = Column(Boolean, nullable=False)
    submitted_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    event = relationship("Event", back_populates="rsvps")

    __table_args__ = (
        UniqueConstraint("event_id", "email", name="unique_rsvp_per_event"),
    )
