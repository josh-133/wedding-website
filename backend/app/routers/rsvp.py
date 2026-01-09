from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api", tags=["rsvp"])


@router.get("/events", response_model=List[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    return events


@router.get("/events/{slug}", response_model=schemas.EventResponse)
def get_event(slug: str, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.slug == slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/rsvp", response_model=schemas.RSVPResponse)
def create_rsvp(rsvp: schemas.RSVPCreate, db: Session = Depends(get_db)):
    # Find the event
    event = db.query(models.Event).filter(models.Event.slug == rsvp.event_slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if RSVP already exists for this email and event
    existing_rsvp = db.query(models.RSVP).filter(
        models.RSVP.event_id == event.id,
        models.RSVP.email == rsvp.email
    ).first()

    if existing_rsvp:
        # Update existing RSVP
        existing_rsvp.name = rsvp.name
        existing_rsvp.attending = rsvp.attending
        db.commit()
        db.refresh(existing_rsvp)
        return existing_rsvp

    # Create new RSVP
    db_rsvp = models.RSVP(
        event_id=event.id,
        name=rsvp.name,
        email=rsvp.email,
        attending=rsvp.attending
    )

    try:
        db.add(db_rsvp)
        db.commit()
        db.refresh(db_rsvp)
        return db_rsvp
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An RSVP for this email already exists for this event"
        )
