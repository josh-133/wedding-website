import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Set test environment variables before importing app
os.environ["ADMIN_PASSWORD"] = "testpassword123"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["REGISTRY_URL"] = "https://test-registry.com"

from app.main import app
from app.database import Base, get_db


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seeded_client(client):
    """Client with seeded test data."""
    from datetime import date
    from app import models

    db = TestingSessionLocal()

    # Add test events
    engagement = models.Event(
        name="Test Engagement Party",
        slug="engagement",
        event_date=date(2026, 5, 23),
        description="Test engagement party"
    )
    wedding = models.Event(
        name="Test Wedding",
        slug="wedding",
        event_date=date(2027, 5, 22),
        description="Test wedding"
    )
    db.add(engagement)
    db.add(wedding)
    db.commit()
    db.close()

    return client


@pytest.fixture
def auth_headers(seeded_client):
    """Get authentication headers for admin endpoints."""
    response = seeded_client.post("/api/admin/login", json={"password": "testpassword123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
