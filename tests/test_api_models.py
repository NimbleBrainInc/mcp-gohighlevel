"""Tests for GoHighLevel API models."""

from mcp_gohighlevel.api_models import (
    Contact,
    ContactListResponse,
    ContactResponse,
    DeleteContactResponse,
    DndSettings,
    UpdateContactResponse,
    UpsertContactResponse,
)


def test_contact_model() -> None:
    """Test Contact model parsing from API response."""
    data = {
        "id": "abc123",
        "firstName": "John",
        "lastName": "Doe",
        "email": "john@example.com",
        "phone": "+1 888-888-8888",
        "locationId": "loc123",
        "companyName": "Acme Inc",
        "tags": ["VIP", "customer"],
        "dateAdded": "2026-01-01T00:00:00Z",
    }
    contact = Contact(**data)
    assert contact.id == "abc123"
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john@example.com"
    assert contact.location_id == "loc123"
    assert contact.company_name == "Acme Inc"
    assert contact.tags == ["VIP", "customer"]


def test_contact_model_minimal() -> None:
    """Test Contact model with only ID."""
    contact = Contact(id="abc123")
    assert contact.id == "abc123"
    assert contact.first_name is None
    assert contact.tags is None


def test_dnd_settings() -> None:
    """Test DND settings model."""
    data = {
        "Call": {"status": "active", "message": "Do not call"},
        "Email": {"status": "inactive"},
    }
    settings = DndSettings(**data)
    assert settings.call is not None
    assert settings.call.status == "active"
    assert settings.email is not None
    assert settings.email.status == "inactive"


def test_contact_response() -> None:
    """Test ContactResponse wrapper."""
    data = {"contact": {"id": "abc123", "firstName": "John"}}
    response = ContactResponse(**data)
    assert response.contact.id == "abc123"


def test_contact_list_response() -> None:
    """Test ContactListResponse."""
    data = {
        "contacts": [
            {"id": "1", "firstName": "Alice"},
            {"id": "2", "firstName": "Bob"},
        ],
        "count": 2,
    }
    response = ContactListResponse(**data)
    assert len(response.contacts) == 2
    assert response.count == 2


def test_contact_list_response_empty() -> None:
    """Test ContactListResponse with empty results."""
    response = ContactListResponse()
    assert response.contacts == []
    assert response.count is None


def test_upsert_response() -> None:
    """Test UpsertContactResponse."""
    data = {
        "new": True,
        "contact": {"id": "new123", "firstName": "New"},
        "traceId": "trace-abc",
    }
    response = UpsertContactResponse(**data)
    assert response.new is True
    assert response.contact.id == "new123"
    assert response.trace_id == "trace-abc"


def test_update_response() -> None:
    """Test UpdateContactResponse."""
    data = {
        "succeded": True,
        "contact": {"id": "abc123", "firstName": "Updated"},
    }
    response = UpdateContactResponse(**data)
    assert response.succeded is True


def test_delete_response() -> None:
    """Test DeleteContactResponse."""
    data = {"succeded": True}
    response = DeleteContactResponse(**data)
    assert response.succeded is True
