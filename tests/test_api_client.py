"""Unit tests for the GoHighLevel API client."""

import os
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from mcp_gohighlevel.api_client import GoHighLevelAPIError, GoHighLevelClient


@pytest_asyncio.fixture
async def mock_client():
    """Create a GoHighLevelClient with mocked session."""
    client = GoHighLevelClient(api_key="test_key")
    client._session = AsyncMock()
    yield client
    await client.close()


class TestClientInitialization:
    """Test client creation and configuration."""

    def test_init_with_explicit_key(self):
        """Client accepts an explicit API key."""
        client = GoHighLevelClient(api_key="explicit_key")
        assert client.api_key == "explicit_key"

    def test_init_with_env_var(self):
        """Client falls back to GOHIGHLEVEL_API_KEY env var."""
        os.environ["GOHIGHLEVEL_API_KEY"] = "env_key"
        try:
            client = GoHighLevelClient()
            assert client.api_key == "env_key"
        finally:
            del os.environ["GOHIGHLEVEL_API_KEY"]

    def test_init_without_key_raises(self):
        """Client raises ValueError when no key is available."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("GOHIGHLEVEL_API_KEY", None)
            with pytest.raises(ValueError, match="GOHIGHLEVEL_API_KEY is required"):
                GoHighLevelClient()

    def test_custom_timeout(self):
        """Client accepts a custom timeout."""
        client = GoHighLevelClient(api_key="key", timeout=60.0)
        assert client.timeout == 60.0

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Client works as an async context manager."""
        async with GoHighLevelClient(api_key="test") as client:
            assert client._session is not None
        assert client._session is None


class TestClientMethods:
    """Test API client methods with mocked responses."""

    @pytest.mark.asyncio
    async def test_get_contact(self, mock_client):
        """Test get contact endpoint."""
        mock_response = {"contact": {"id": "abc123", "firstName": "John"}}
        with patch.object(mock_client, "_request", return_value=mock_response):
            result = await mock_client.get_contact("abc123")
        assert result["contact"]["id"] == "abc123"

    @pytest.mark.asyncio
    async def test_create_contact(self, mock_client):
        """Test create contact endpoint."""
        mock_response = {"contact": {"id": "new123", "firstName": "Jane"}}
        data = {"locationId": "loc123", "firstName": "Jane"}
        with patch.object(mock_client, "_request", return_value=mock_response):
            result = await mock_client.create_contact(data)
        assert result["contact"]["id"] == "new123"

    @pytest.mark.asyncio
    async def test_delete_contact(self, mock_client):
        """Test delete contact endpoint."""
        mock_response = {"succeded": True}
        with patch.object(mock_client, "_request", return_value=mock_response):
            result = await mock_client.delete_contact("abc123")
        assert result["succeded"] is True

    @pytest.mark.asyncio
    async def test_list_contacts(self, mock_client):
        """Test list contacts endpoint."""
        mock_response = {"contacts": [{"id": "1"}], "count": 1}
        with patch.object(mock_client, "_request", return_value=mock_response):
            result = await mock_client.list_contacts(location_id="loc123", limit=10)
        assert len(result["contacts"]) == 1

    @pytest.mark.asyncio
    async def test_search_contacts(self, mock_client):
        """Test search contacts endpoint."""
        mock_response = {"contacts": [{"id": "1"}]}
        data = {"locationId": "loc123", "query": "John"}
        with patch.object(mock_client, "_request", return_value=mock_response):
            result = await mock_client.search_contacts(data)
        assert len(result["contacts"]) == 1


class TestErrorHandling:
    """Test error handling for API errors."""

    @pytest.mark.asyncio
    async def test_401_unauthorized(self, mock_client):
        """Test handling of unauthorized errors."""
        with patch.object(
            mock_client,
            "_request",
            side_effect=GoHighLevelAPIError(401, "Invalid API key"),
        ):
            with pytest.raises(GoHighLevelAPIError) as exc_info:
                await mock_client.get_contact("abc123")
            assert exc_info.value.status == 401

    @pytest.mark.asyncio
    async def test_422_unprocessable(self, mock_client):
        """Test handling of validation errors."""
        with patch.object(
            mock_client,
            "_request",
            side_effect=GoHighLevelAPIError(422, "Validation failed"),
        ):
            with pytest.raises(GoHighLevelAPIError) as exc_info:
                await mock_client.create_contact({"locationId": "loc123"})
            assert exc_info.value.status == 422

    @pytest.mark.asyncio
    async def test_network_error(self, mock_client):
        """Test handling of network errors."""
        with patch.object(
            mock_client,
            "_request",
            side_effect=GoHighLevelAPIError(500, "Network error: Connection failed"),
        ):
            with pytest.raises(GoHighLevelAPIError) as exc_info:
                await mock_client.get_contact("abc123")
            assert exc_info.value.status == 500
            assert "Network error" in exc_info.value.message

    def test_error_string_representation(self):
        """Test error string format."""
        err = GoHighLevelAPIError(401, "Unauthorized", {"id": "auth_error"})
        assert "401" in str(err)
        assert "Unauthorized" in str(err)
        assert err.details == {"id": "auth_error"}
