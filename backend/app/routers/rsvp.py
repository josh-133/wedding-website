from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from .. import models, schemas
from ..database import get_db
from ..email import send_rsvp_confirmation

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


def create_guests_for_rsvp(
    db: Session,
    rsvp: models.RSVP,
    primary_name: str,
    primary_dietary: str | None,
    additional_guests: List[schemas.GuestCreate]
) -> None:
    """Create guest records for an RSVP, including the primary contact."""
    # Delete existing guests if updating
    db.query(models.Guest).filter(models.Guest.rsvp_id == rsvp.id).delete()

    # Create primary guest
    primary_guest = models.Guest(
        rsvp_id=rsvp.id,
        name=primary_name,
        dietary_requirements=primary_dietary,
        is_primary=True
    )
    db.add(primary_guest)

    # Create additional guests
    for guest_data in additional_guests:
        guest = models.Guest(
            rsvp_id=rsvp.id,
            name=guest_data.name,
            dietary_requirements=guest_data.dietary_requirements,
            is_primary=False
        )
        db.add(guest)


@router.post("/rsvp", response_model=schemas.RSVPResponse)
def create_rsvp(
    rsvp: schemas.RSVPCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Find the event
    event = db.query(models.Event).filter(models.Event.slug == rsvp.event_slug).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Calculate total guest count (primary + additional guests)
    guest_count = 1 + len(rsvp.guests)

    # Use the primary contact's dietary requirements from the RSVP
    primary_dietary = rsvp.dietary_requirements
    additional_guests = rsvp.guests

    # Check if RSVP already exists for this email and event
    existing_rsvp = db.query(models.RSVP).filter(
        models.RSVP.event_id == event.id,
        models.RSVP.email == rsvp.email
    ).first()

    if existing_rsvp:
        # Update existing RSVP
        existing_rsvp.name = rsvp.name
        existing_rsvp.postal_address = rsvp.postal_address
        existing_rsvp.attending = rsvp.attending
        existing_rsvp.guest_count = guest_count

        # Update guests
        create_guests_for_rsvp(
            db, existing_rsvp, rsvp.name, primary_dietary, additional_guests
        )

        db.commit()
        db.refresh(existing_rsvp)

        # Collect all guest names for email
        guest_names = [rsvp.name] + [g.name for g in additional_guests]

        # Send confirmation email in background
        background_tasks.add_task(
            send_rsvp_confirmation,
            to_email=rsvp.email,
            guest_name=rsvp.name,
            event_name=event.name,
            event_slug=event.slug,
            event_date=event.event_date,
            attending=rsvp.attending,
            guest_names=guest_names,
            guest_count=guest_count
        )

        return existing_rsvp

    # Create new RSVP
    db_rsvp = models.RSVP(
        event_id=event.id,
        name=rsvp.name,
        email=rsvp.email,
        postal_address=rsvp.postal_address,
        attending=rsvp.attending,
        guest_count=guest_count
    )

    try:
        db.add(db_rsvp)
        db.flush()  # Get the ID without committing

        # Create guests
        create_guests_for_rsvp(
            db, db_rsvp, rsvp.name, primary_dietary, additional_guests
        )

        db.commit()
        db.refresh(db_rsvp)

        # Collect all guest names for email
        guest_names = [rsvp.name] + [g.name for g in additional_guests]

        # Send confirmation email in background
        background_tasks.add_task(
            send_rsvp_confirmation,
            to_email=rsvp.email,
            guest_name=rsvp.name,
            event_name=event.name,
            event_slug=event.slug,
            event_date=event.event_date,
            attending=rsvp.attending,
            guest_names=guest_names,
            guest_count=guest_count
        )

        return db_rsvp
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An RSVP for this email already exists for this event"
        )
