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
    query = db.query(
        models.RSVP.id,
        models.RSVP.name,
        models.RSVP.email,
        models.RSVP.attending,
        models.RSVP.submitted_at,
        models.Event.name.label("event_name"),
        models.Event.slug.label("event_slug")
    ).join(models.Event)

    if event_slug:
        query = query.filter(models.Event.slug == event_slug)

    results = query.order_by(models.RSVP.submitted_at.desc()).all()

    return [
        schemas.RSVPListResponse(
            id=r.id,
            name=r.name,
            email=r.email,
            attending=r.attending,
            submitted_at=r.submitted_at,
            event_name=r.event_name,
            event_slug=r.event_slug
        )
        for r in results
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

        stats.append(schemas.StatsResponse(
            event_slug=event.slug,
            event_name=event.name,
            total_responses=total,
            attending=attending,
            not_attending=total - attending
        ))

    return stats


@router.get("/rsvps/export")
def export_rsvps(
    event_slug: Optional[str] = None,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_token)
):
    query = db.query(
        models.RSVP.name,
        models.RSVP.email,
        models.RSVP.attending,
        models.RSVP.submitted_at,
        models.Event.name.label("event_name")
    ).join(models.Event)

    if event_slug:
        query = query.filter(models.Event.slug == event_slug)

    results = query.order_by(models.Event.name, models.RSVP.submitted_at).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Event", "Name", "Email", "Attending", "Submitted At"])

    for r in results:
        writer.writerow([
            r.event_name,
            r.name,
            r.email,
            "Yes" if r.attending else "No",
            r.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    output.seek(0)

    filename = f"rsvps_{event_slug}.csv" if event_slug else "rsvps_all.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
