"""Shared fixtures for unit tests."""

from unittest.mock import AsyncMock

import pytest

from mcp_gohighlevel.server import mcp


@pytest.fixture
def mcp_server():
    """Return the MCP server instance."""
    return mcp


@pytest.fixture
def mock_client():
    """Create a mock API client."""
    client = AsyncMock()
    client.get_contact = AsyncMock(
        return_value={
            "contact": {
                "id": "abc123",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
                "locationId": "loc123",
            }
        }
    )
    client.create_contact = AsyncMock(
        return_value={
            "contact": {
                "id": "new123",
                "firstName": "Jane",
                "lastName": "Doe",
                "email": "jane@example.com",
                "locationId": "loc123",
            }
        }
    )
    client.update_contact = AsyncMock(
        return_value={
            "succeded": True,
            "contact": {
                "id": "abc123",
                "firstName": "John",
                "lastName": "Smith",
                "locationId": "loc123",
            },
        }
    )
    client.delete_contact = AsyncMock(return_value={"succeded": True})
    client.upsert_contact = AsyncMock(
        return_value={
            "new": True,
            "contact": {
                "id": "upsert123",
                "firstName": "Upserted",
                "locationId": "loc123",
            },
        }
    )
    client.list_contacts = AsyncMock(
        return_value={
            "contacts": [
                {"id": "1", "firstName": "Alice"},
                {"id": "2", "firstName": "Bob"},
            ],
            "count": 2,
        }
    )
    client.search_contacts = AsyncMock(
        return_value={
            "contacts": [{"id": "1", "firstName": "Alice"}],
        }
    )
    return client
