from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date
import os
import logging

logger = logging.getLogger(__name__)

# Use DATABASE_URL from environment, with fallback to local data directory
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Local development fallback
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'wedding.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_migrations():
    """Add new columns to existing tables if they don't exist."""
    inspector = inspect(engine)
    if "rsvps" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("rsvps")]
        if "postal_address" not in columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE rsvps ADD COLUMN postal_address VARCHAR(500)"))
            logger.info("Added postal_address column to rsvps table")


def init_db():
    from . import models
    Base.metadata.create_all(bind=engine)
    run_migrations()

    # Seed initial data
    db = SessionLocal()
    try:
        # Check if events exist
        if not db.query(models.Event).first():
            engagement = models.Event(
                name="Engagement Party",
                slug="engagement",
                event_date=date(2026, 5, 23),
                description="Join us to celebrate our engagement!"
            )
            wedding = models.Event(
                name="Wedding",
                slug="wedding",
                event_date=date(2027, 5, 22),
                description="We invite you to celebrate our wedding day."
            )
            db.add(engagement)
            db.add(wedding)
            db.commit()
    finally:
        db.close()
