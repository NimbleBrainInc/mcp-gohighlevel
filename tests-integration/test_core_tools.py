"""
Core tools integration tests.

Tests basic API functionality with real GoHighLevel API calls.
Requires GOHIGHLEVEL_API_KEY environment variable.
"""

# import pytest
# from mcp_gohighlevel.api_client import GoHighLevelAPIError, GoHighLevelClient


# TODO: Add integration tests for each tool group. Example:
#
# class TestListContacts:
#     """Test list contacts endpoint."""
#
#     @pytest.mark.asyncio
#     async def test_list_contacts(self, client: GoHighLevelClient):
#         """Test listing contacts."""
#         result = await client.list_contacts(location_id="your_location_id", limit=5)
#         assert "contacts" in result
#         print(f"Found {len(result['contacts'])} contacts")
