from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import timedelta, datetime
from collections import defaultdict
import csv
import io
from .. import models, schemas, config
from ..database import get_db
from ..auth import verify_password, create_access_token, verify_token

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Simple in-memory rate limiting for login attempts
# In production, consider using Redis for distributed rate limiting
login_attempts: dict[str, list[datetime]] = defaultdict(list)
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300  # 5 minutes


def check_rate_limit(ip: str) -> bool:
    """Check if IP has exceeded login rate limit. Returns True if allowed."""
    now = datetime.now()
    # Clean old attempts
    login_attempts[ip] = [
        attempt for attempt in login_attempts[ip]
        if (now - attempt).total_seconds() < LOGIN_WINDOW_SECONDS
    ]
    return len(login_attempts[ip]) < MAX_LOGIN_ATTEMPTS


def record_login_attempt(ip: str):
    """Record a failed login attempt."""
    login_attempts[ip].append(datetime.now())


@router.post("/login", response_model=schemas.AdminToken)
def login(credentials: schemas.AdminLogin, request: Request):
    client_ip = request.client.host if request.client else "unknown"

    # Check rate limit
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    if not verify_password(credentials.password):
        record_login_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Clear attempts on successful login
    login_attempts.pop(client_ip, None)

    access_token = create_access_token(
        data={"sub": "admin"},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return schemas.AdminToken(access_token=access_token)


@router.get("/rsvps", response_model=List[schemas.RSVPListResponse])
def get_rsvps(
    event_slug: Optional[str] = None,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    query = db.query(models.RSVP).join(models.Event)

    if event_slug:
        query = query.filter(models.Event.slug == event_slug)

    rsvps = query.order_by(models.RSVP.submitted_at.desc()).all()

    return [
        schemas.RSVPListResponse(
            id=rsvp.id,
            name=rsvp.name,
            email=rsvp.email,
            postal_address=rsvp.postal_address,
            attending=rsvp.attending,
            guest_count=rsvp.guest_count,
            submitted_at=rsvp.submitted_at,
            event_name=rsvp.event.name,
            event_slug=rsvp.event.slug,
            guests=[
                schemas.GuestResponse(
                    id=guest.id,
                    name=guest.name,
                    dietary_requirements=guest.dietary_requirements,
                    is_primary=guest.is_primary
                )
                for guest in rsvp.guests
            ]
        )
        for rsvp in rsvps
    ]


@router.get("/stats", response_model=List[schemas.StatsResponse])
def get_stats(db: Session = Depends(get_db), _: bool = Depends(verify_token)):
    events = db.query(models.Event).all()
    stats = []

    for event in events:
        total = db.query(models.RSVP).filter(models.RSVP.event_id == event.id).count()
        attending = db.query(models.RSVP).filter(
            models.RSVP.event_id == event.id,
            models.RSVP.attending == True
        ).count()

        # Sum up total guests (not just RSVPs)
        guests_attending = db.query(func.sum(models.RSVP.guest_count)).filter(
            models.RSVP.event_id == event.id,
            models.RSVP.attending == True
        ).scalar() or 0

        guests_not_attending = db.query(func.sum(models.RSVP.guest_count)).filter(
            models.RSVP.event_id == event.id,
            models.RSVP.attending == False
        ).scalar() or 0

        stats.append(schemas.StatsResponse(
            event_slug=event.slug,
            event_name=event.name,
            total_responses=total,
            attending=attending,
            not_attending=total - attending,
            total_guests_attending=guests_attending,
            total_guests_not_attending=guests_not_attending
        ))

    return stats


@router.delete("/rsvps/{rsvp_id}")
def delete_rsvp(
    rsvp_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    """Delete an RSVP and all associated guests."""
    rsvp = db.query(models.RSVP).filter(models.RSVP.id == rsvp_id).first()

    if not rsvp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RSVP not found"
        )

    # Delete associated guests first
    db.query(models.Guest).filter(models.Guest.rsvp_id == rsvp_id).delete()

    # Delete the RSVP
    db.delete(rsvp)
    db.commit()

    return {"message": "RSVP deleted successfully"}


@router.get("/rsvps/export")
def export_rsvps(
    event_slug: Optional[str] = None,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    query = db.query(models.RSVP).join(models.Event)

    if event_slug:
        query = query.filter(models.Event.slug == event_slug)

    rsvps = query.order_by(models.Event.name, models.RSVP.submitted_at).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Event", "Primary Contact", "Email", "Postal Address", "Attending",
        "Guest Count", "Guest Name", "Dietary Requirements",
        "Is Primary", "Submitted At"
    ])

    for rsvp in rsvps:
        # Write a row for each guest
        for guest in rsvp.guests:
            writer.writerow([
                rsvp.event.name,
                rsvp.name,
                rsvp.email,
                rsvp.postal_address or "",
                "Yes" if rsvp.attending else "No",
                rsvp.guest_count,
                guest.name,
                guest.dietary_requirements or "",
                "Yes" if guest.is_primary else "No",
                rsvp.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
            ])
        # If no guests (legacy data), still write the RSVP
        if not rsvp.guests:
            writer.writerow([
                rsvp.event.name,
                rsvp.name,
                rsvp.email,
                rsvp.postal_address or "",
                "Yes" if rsvp.attending else "No",
                rsvp.guest_count,
                rsvp.name,
                "",
                "Yes",
                rsvp.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

    output.seek(0)

    filename = f"rsvps_{event_slug}.csv" if event_slug else "rsvps_all.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
