from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import timedelta
import csv
import io
from .. import models, schemas, config
from ..database import get_db
from ..auth import verify_password, create_access_token, verify_token

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=schemas.AdminToken)
def login(credentials: schemas.AdminLogin):
    if not verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
