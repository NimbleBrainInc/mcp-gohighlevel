"""Tests for GoHighLevel MCP Server tools and skill resource."""

from unittest.mock import patch

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from mcp_gohighlevel.api_client import GoHighLevelAPIError
from mcp_gohighlevel.server import SKILL_CONTENT


class TestSkillResource:
    """Test the skill resource and server instructions."""

    @pytest.mark.asyncio
    async def test_initialize_returns_instructions(self, mcp_server):
        """Server instructions reference the skill resource."""
        async with Client(mcp_server) as client:
            result = await client.initialize()
            assert result.instructions is not None
            assert "skill://gohighlevel/usage" in result.instructions

    @pytest.mark.asyncio
    async def test_skill_resource_listed(self, mcp_server):
        """skill://gohighlevel/usage appears in resource listing."""
        async with Client(mcp_server) as client:
            resources = await client.list_resources()
            uris = [str(r.uri) for r in resources]
            assert "skill://gohighlevel/usage" in uris

    @pytest.mark.asyncio
    async def test_skill_resource_readable(self, mcp_server):
        """Reading the skill resource returns the full skill content."""
        async with Client(mcp_server) as client:
            contents = await client.read_resource("skill://gohighlevel/usage")
            text = contents[0].text if hasattr(contents[0], "text") else str(contents[0])
            assert "get_contact" in text
            assert "create_contact" in text

    @pytest.mark.asyncio
    async def test_skill_content_matches_constant(self, mcp_server):
        """Resource content matches the SKILL_CONTENT constant."""
        async with Client(mcp_server) as client:
            contents = await client.read_resource("skill://gohighlevel/usage")
            text = contents[0].text if hasattr(contents[0], "text") else str(contents[0])
            assert text == SKILL_CONTENT


class TestToolListing:
    """Test that all tools are registered and discoverable."""

    @pytest.mark.asyncio
    async def test_all_tools_listed(self, mcp_server):
        """All expected tools appear in tool listing."""
        async with Client(mcp_server) as client:
            tools = await client.list_tools()
            names = {t.name for t in tools}
            expected = {
                "get_contact",
                "create_contact",
                "update_contact",
                "delete_contact",
                "upsert_contact",
                "list_contacts",
                "search_contacts",
            }
            assert expected == names


class TestMCPTools:
    """Test the MCP server tools via FastMCP Client."""

    @pytest.mark.asyncio
    async def test_get_contact(self, mcp_server, mock_client):
        """Test get_contact tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool("get_contact", {"contact_id": "abc123"})
            assert result is not None
            mock_client.get_contact.assert_called_once_with("abc123")

    @pytest.mark.asyncio
    async def test_create_contact(self, mcp_server, mock_client):
        """Test create_contact tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool(
                    "create_contact",
                    {
                        "location_id": "loc123",
                        "first_name": "Jane",
                        "email": "jane@example.com",
                    },
                )
            assert result is not None
            mock_client.create_contact.assert_called_once()
            call_data = mock_client.create_contact.call_args[0][0]
            assert call_data["locationId"] == "loc123"
            assert call_data["firstName"] == "Jane"
            assert call_data["email"] == "jane@example.com"

    @pytest.mark.asyncio
    async def test_update_contact(self, mcp_server, mock_client):
        """Test update_contact tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool(
                    "update_contact",
                    {"contact_id": "abc123", "last_name": "Smith"},
                )
            assert result is not None
            mock_client.update_contact.assert_called_once_with("abc123", {"lastName": "Smith"})

    @pytest.mark.asyncio
    async def test_delete_contact(self, mcp_server, mock_client):
        """Test delete_contact tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool("delete_contact", {"contact_id": "abc123"})
            assert result is not None
            mock_client.delete_contact.assert_called_once_with("abc123")

    @pytest.mark.asyncio
    async def test_upsert_contact(self, mcp_server, mock_client):
        """Test upsert_contact tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool(
                    "upsert_contact",
                    {
                        "location_id": "loc123",
                        "email": "test@example.com",
                    },
                )
            assert result is not None
            call_data = mock_client.upsert_contact.call_args[0][0]
            assert call_data["locationId"] == "loc123"
            assert call_data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_list_contacts(self, mcp_server, mock_client):
        """Test list_contacts tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool(
                    "list_contacts",
                    {"location_id": "loc123", "limit": 10},
                )
            assert result is not None
            mock_client.list_contacts.assert_called_once_with(
                location_id="loc123",
                query=None,
                limit=10,
                start_after_id=None,
                start_after=None,
            )

    @pytest.mark.asyncio
    async def test_search_contacts(self, mcp_server, mock_client):
        """Test search_contacts tool."""
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                result = await client.call_tool(
                    "search_contacts",
                    {"location_id": "loc123", "query": "John"},
                )
            assert result is not None
            call_data = mock_client.search_contacts.call_args[0][0]
            assert call_data["locationId"] == "loc123"
            assert call_data["query"] == "John"

    @pytest.mark.asyncio
    async def test_get_contact_api_error(self, mcp_server, mock_client):
        """Test get_contact handles API errors."""
        mock_client.get_contact.side_effect = GoHighLevelAPIError(401, "Unauthorized")
        with patch("mcp_gohighlevel.server.get_client", return_value=mock_client):
            async with Client(mcp_server) as client:
                with pytest.raises(ToolError, match="401"):
                    await client.call_tool("get_contact", {"contact_id": "abc123"})
