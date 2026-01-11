"""Tests for the Wedding RSVP API."""
import pytest


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_welcome_message(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Wedding RSVP API", "docs": "/docs"}


class TestEventsEndpoints:
    """Tests for events endpoints."""

    def test_get_events_empty(self, client):
        response = client.get("/api/events")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_events_with_data(self, seeded_client):
        response = seeded_client.get("/api/events")
        assert response.status_code == 200
        events = response.json()
        assert len(events) == 2
        slugs = [e["slug"] for e in events]
        assert "engagement" in slugs
        assert "wedding" in slugs

    def test_get_event_by_slug(self, seeded_client):
        response = seeded_client.get("/api/events/engagement")
        assert response.status_code == 200
        event = response.json()
        assert event["slug"] == "engagement"
        assert event["name"] == "Test Engagement Party"

    def test_get_event_not_found(self, seeded_client):
        response = seeded_client.get("/api/events/nonexistent")
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"


class TestRSVPEndpoints:
    """Tests for RSVP endpoints."""

    def test_create_rsvp_attending(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Doe",
            "email": "john@example.com",
            "attending": True
        })
        assert response.status_code == 200
        rsvp = response.json()
        assert rsvp["name"] == "John Doe"
        assert rsvp["email"] == "john@example.com"
        assert rsvp["attending"] is True

    def test_create_rsvp_not_attending(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "engagement",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "attending": False
        })
        assert response.status_code == 200
        rsvp = response.json()
        assert rsvp["attending"] is False

    def test_create_rsvp_invalid_event(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "nonexistent",
            "name": "Test User",
            "email": "test@example.com",
            "attending": True
        })
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"

    def test_create_rsvp_invalid_email(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Test User",
            "email": "invalid-email",
            "attending": True
        })
        assert response.status_code == 422  # Validation error

    def test_create_rsvp_update_existing(self, seeded_client):
        # First RSVP
        response1 = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Doe",
            "email": "john@example.com",
            "attending": True
        })
        assert response1.status_code == 200
        assert response1.json()["attending"] is True

        # Update RSVP (same email, same event)
        response2 = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Doe Updated",
            "email": "john@example.com",
            "attending": False
        })
        assert response2.status_code == 200
        assert response2.json()["attending"] is False
        assert response2.json()["name"] == "John Doe Updated"

    def test_create_rsvp_same_email_different_events(self, seeded_client):
        # RSVP for engagement
        response1 = seeded_client.post("/api/rsvp", json={
            "event_slug": "engagement",
            "name": "John Doe",
            "email": "john@example.com",
            "attending": True
        })
        assert response1.status_code == 200

        # RSVP for wedding (same email, different event - should work)
        response2 = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Doe",
            "email": "john@example.com",
            "attending": True
        })
        assert response2.status_code == 200

    def test_create_rsvp_empty_name(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "",
            "email": "test@example.com",
            "attending": True
        })
        assert response.status_code == 422  # Validation error

    def test_create_rsvp_name_with_html_stripped(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "<script>alert('xss')</script>John",
            "email": "test@example.com",
            "attending": True
        })
        assert response.status_code == 200
        # HTML should be stripped
        assert "<script>" not in response.json()["name"]

    def test_create_rsvp_invalid_event_slug_format(self, seeded_client):
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "invalid slug with spaces",
            "name": "Test User",
            "email": "test@example.com",
            "attending": True
        })
        assert response.status_code == 422  # Validation error

    def test_create_rsvp_with_guests(self, seeded_client):
        """Test RSVP with multiple guests."""
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Smith",
            "email": "john@example.com",
            "attending": True,
            "guests": [
                {"name": "Jane Smith", "dietary_requirements": "Vegetarian"},
                {"name": "Tommy Smith", "dietary_requirements": None}
            ]
        })
        assert response.status_code == 200
        rsvp = response.json()
        assert rsvp["guest_count"] == 3
        assert len(rsvp["guests"]) == 3  # Primary + 2 additional
        guest_names = [g["name"] for g in rsvp["guests"]]
        assert "John Smith" in guest_names
        assert "Jane Smith" in guest_names
        assert "Tommy Smith" in guest_names

    def test_create_rsvp_max_guests(self, seeded_client):
        """Test that max 5 guests are allowed."""
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Primary Guest",
            "email": "primary@example.com",
            "attending": True,
            "guests": [
                {"name": "Guest 2"},
                {"name": "Guest 3"},
                {"name": "Guest 4"},
                {"name": "Guest 5"}
            ]
        })
        assert response.status_code == 200
        assert response.json()["guest_count"] == 5

    def test_create_rsvp_exceeds_max_guests(self, seeded_client):
        """Test that more than 5 guests are rejected."""
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Primary Guest",
            "email": "primary@example.com",
            "attending": True,
            "guests": [
                {"name": "Guest 2"},
                {"name": "Guest 3"},
                {"name": "Guest 4"},
                {"name": "Guest 5"},
                {"name": "Guest 6"}  # This exceeds the limit
            ]
        })
        assert response.status_code == 422  # Validation error

    def test_create_rsvp_not_attending_with_guests(self, seeded_client):
        """Test declining RSVP with multiple guests."""
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Doe",
            "email": "john@example.com",
            "attending": False,
            "guests": [
                {"name": "Jane Doe"}
            ]
        })
        assert response.status_code == 200
        rsvp = response.json()
        assert rsvp["attending"] is False
        assert rsvp["guest_count"] == 2

    def test_update_rsvp_with_guests(self, seeded_client):
        """Test updating an RSVP changes guest list."""
        # First RSVP with 2 guests
        response1 = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Smith",
            "email": "john@example.com",
            "attending": True,
            "guests": [{"name": "Jane Smith"}]
        })
        assert response1.json()["guest_count"] == 2

        # Update with 3 guests
        response2 = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Smith",
            "email": "john@example.com",
            "attending": True,
            "guests": [
                {"name": "Jane Smith"},
                {"name": "Tommy Smith"}
            ]
        })
        assert response2.json()["guest_count"] == 3
        assert len(response2.json()["guests"]) == 3

    def test_guest_dietary_requirements_sanitized(self, seeded_client):
        """Test that dietary requirements have HTML stripped."""
        response = seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "John Smith",
            "email": "john@example.com",
            "attending": True,
            "guests": [
                {"name": "Jane Smith", "dietary_requirements": "<script>alert('xss')</script>Vegetarian"}
            ]
        })
        assert response.status_code == 200
        guest = next(g for g in response.json()["guests"] if g["name"] == "Jane Smith")
        assert "<script>" not in guest["dietary_requirements"]


class TestRegistryEndpoint:
    """Tests for registry endpoint."""

    def test_get_registry(self, client):
        response = client.get("/api/registry")
        assert response.status_code == 200
        assert "registry_url" in response.json()


class TestAdminEndpoints:
    """Tests for admin endpoints."""

    def test_admin_login_success(self, seeded_client):
        response = seeded_client.post("/api/admin/login", json={
            "password": "testpassword123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_admin_login_wrong_password(self, seeded_client):
        response = seeded_client.post("/api/admin/login", json={
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect password"

    def test_admin_get_rsvps_unauthorized(self, seeded_client):
        response = seeded_client.get("/api/admin/rsvps")
        assert response.status_code == 401  # No authorization header

    def test_admin_get_rsvps_authorized(self, seeded_client, auth_headers):
        # First create an RSVP
        seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Test Guest",
            "email": "guest@example.com",
            "attending": True
        })

        response = seeded_client.get("/api/admin/rsvps", headers=auth_headers)
        assert response.status_code == 200
        rsvps = response.json()
        assert len(rsvps) == 1
        assert rsvps[0]["name"] == "Test Guest"

    def test_admin_get_rsvps_filter_by_event(self, seeded_client, auth_headers):
        # Create RSVPs for different events
        seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Wedding Guest",
            "email": "wedding@example.com",
            "attending": True
        })
        seeded_client.post("/api/rsvp", json={
            "event_slug": "engagement",
            "name": "Engagement Guest",
            "email": "engagement@example.com",
            "attending": True
        })

        # Filter by wedding
        response = seeded_client.get("/api/admin/rsvps?event_slug=wedding", headers=auth_headers)
        assert response.status_code == 200
        rsvps = response.json()
        assert len(rsvps) == 1
        assert rsvps[0]["event_slug"] == "wedding"

    def test_admin_get_stats(self, seeded_client, auth_headers):
        # Create some RSVPs with guests
        seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Guest 1",
            "email": "guest1@example.com",
            "attending": True,
            "guests": [{"name": "Guest 1 Partner"}]  # 2 guests attending
        })
        seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Guest 2",
            "email": "guest2@example.com",
            "attending": False,
            "guests": [{"name": "Guest 2 Partner"}, {"name": "Guest 2 Child"}]  # 3 not attending
        })

        response = seeded_client.get("/api/admin/stats", headers=auth_headers)
        assert response.status_code == 200
        stats = response.json()
        assert len(stats) == 2

        wedding_stats = next(s for s in stats if s["event_slug"] == "wedding")
        assert wedding_stats["total_responses"] == 2
        assert wedding_stats["attending"] == 1
        assert wedding_stats["not_attending"] == 1
        assert wedding_stats["total_guests_attending"] == 2
        assert wedding_stats["total_guests_not_attending"] == 3

    def test_admin_export_rsvps(self, seeded_client, auth_headers):
        # Create an RSVP
        seeded_client.post("/api/rsvp", json={
            "event_slug": "wedding",
            "name": "Export Test",
            "email": "export@example.com",
            "attending": True
        })

        response = seeded_client.get("/api/admin/rsvps/export", headers=auth_headers)
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]

        # Check CSV content
        content = response.content.decode()
        assert "Export Test" in content
        assert "export@example.com" in content
        assert "Yes" in content


class TestRateLimiting:
    """Tests for rate limiting on login endpoint."""

    def test_rate_limit_after_failed_attempts(self, seeded_client):
        # Make multiple failed login attempts
        for _ in range(5):
            seeded_client.post("/api/admin/login", json={"password": "wrong"})

        # The 6th attempt should be rate limited
        response = seeded_client.post("/api/admin/login", json={"password": "wrong"})
        assert response.status_code == 429
        assert "Too many login attempts" in response.json()["detail"]


class TestSecurityConfig:
    """Tests for security configuration."""

    def test_admin_login_disabled_when_no_password(self, seeded_client, monkeypatch):
        """Test that admin login fails when ADMIN_PASSWORD is not set."""
        from app import config
        from app.routers import admin

        # Clear any existing rate limiting
        admin.login_attempts.clear()

        monkeypatch.setattr(config, "ADMIN_PASSWORD", "")

        response = seeded_client.post("/api/admin/login", json={"password": "anypassword"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect password"
