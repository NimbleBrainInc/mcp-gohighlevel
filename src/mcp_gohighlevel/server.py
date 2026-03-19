"""GoHighLevel MCP Server - FastMCP Implementation.

Contact management: get, create, update, delete, upsert, list, search.
"""

import logging
import os
import sys
from importlib.resources import files
from typing import Any

from fastmcp import Context, FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp_gohighlevel.api_client import GoHighLevelAPIError, GoHighLevelClient

# Logging setup - all logs to stderr (stdout is reserved for JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("mcp_gohighlevel")

logger.info("GoHighLevel server module loading...")

SKILL_CONTENT = files("mcp_gohighlevel").joinpath("SKILL.md").read_text()

# Create MCP server
mcp = FastMCP(
    "GoHighLevel",
    instructions=(
        "Before using tools, read the skill://gohighlevel/usage resource "
        "for tool selection guidance and workflow patterns."
    ),
)

# Global client instance (lazy initialization)
_client: GoHighLevelClient | None = None


async def get_client(ctx: Context | None = None) -> GoHighLevelClient:
    """Get or create the API client instance."""
    global _client
    if _client is None:
        api_key = os.environ.get("GOHIGHLEVEL_API_KEY")
        if not api_key:
            msg = "GOHIGHLEVEL_API_KEY environment variable is required"
            if ctx:
                await ctx.error(msg)
            raise ValueError(msg)
        _client = GoHighLevelClient(api_key=api_key)
    return _client


# Health endpoint for HTTP transport
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse({"status": "healthy", "service": "mcp-gohighlevel"})


# ============================================================================
# Tools
# ============================================================================


@mcp.tool()
async def get_contact(
    contact_id: str,
    ctx: Context | None = None,
) -> dict:
    """Get a single contact by ID.

    Args:
        contact_id: The GoHighLevel contact ID
        ctx: MCP context for logging

    Returns:
        Contact details including name, email, phone, tags, custom fields, etc.
    """
    client = await get_client(ctx)
    try:
        return await client.get_contact(contact_id)
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def create_contact(
    location_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    company_name: str | None = None,
    website: str | None = None,
    address1: str | None = None,
    city: str | None = None,
    state: str | None = None,
    postal_code: str | None = None,
    country: str | None = None,
    timezone: str | None = None,
    tags: list[str] | None = None,
    source: str | None = None,
    dnd: bool | None = None,
    assigned_to: str | None = None,
    date_of_birth: str | None = None,
    ctx: Context | None = None,
) -> dict:
    """Create a new contact in GoHighLevel.

    Args:
        location_id: The location (sub-account) ID (required)
        first_name: First name
        last_name: Last name
        name: Full name (alternative to first/last)
        email: Email address
        phone: Phone number
        company_name: Company name
        website: Website URL
        address1: Street address
        city: City
        state: State
        postal_code: Postal code
        country: Country
        timezone: Timezone
        tags: List of tags
        source: Lead source
        dnd: Do-not-disturb flag
        assigned_to: User ID to assign contact to
        date_of_birth: Date of birth
        ctx: MCP context for logging

    Returns:
        The created contact
    """
    client = await get_client(ctx)
    data: dict[str, Any] = {"locationId": location_id}

    field_map = {
        "firstName": first_name,
        "lastName": last_name,
        "name": name,
        "email": email,
        "phone": phone,
        "companyName": company_name,
        "website": website,
        "address1": address1,
        "city": city,
        "state": state,
        "postalCode": postal_code,
        "country": country,
        "timezone": timezone,
        "tags": tags,
        "source": source,
        "dnd": dnd,
        "assignedTo": assigned_to,
        "dateOfBirth": date_of_birth,
    }

    for key, value in field_map.items():
        if value is not None:
            data[key] = value

    try:
        return await client.create_contact(data)
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def update_contact(
    contact_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    company_name: str | None = None,
    website: str | None = None,
    address1: str | None = None,
    city: str | None = None,
    state: str | None = None,
    postal_code: str | None = None,
    country: str | None = None,
    timezone: str | None = None,
    tags: list[str] | None = None,
    source: str | None = None,
    dnd: bool | None = None,
    assigned_to: str | None = None,
    date_of_birth: str | None = None,
    ctx: Context | None = None,
) -> dict:
    """Update an existing contact. Only provided fields are changed.

    WARNING: tags overwrites ALL existing tags. To add/remove individual tags,
    use the GHL Tags API directly.

    Args:
        contact_id: The contact ID to update
        first_name: First name
        last_name: Last name
        name: Full name
        email: Email address
        phone: Phone number
        company_name: Company name
        website: Website URL
        address1: Street address
        city: City
        state: State
        postal_code: Postal code
        country: Country
        timezone: Timezone
        tags: List of tags (REPLACES all existing tags)
        source: Lead source
        dnd: Do-not-disturb flag
        assigned_to: User ID to assign contact to
        date_of_birth: Date of birth
        ctx: MCP context for logging

    Returns:
        The updated contact with succeded flag
    """
    client = await get_client(ctx)
    data: dict[str, Any] = {}

    field_map = {
        "firstName": first_name,
        "lastName": last_name,
        "name": name,
        "email": email,
        "phone": phone,
        "companyName": company_name,
        "website": website,
        "address1": address1,
        "city": city,
        "state": state,
        "postalCode": postal_code,
        "country": country,
        "timezone": timezone,
        "tags": tags,
        "source": source,
        "dnd": dnd,
        "assignedTo": assigned_to,
        "dateOfBirth": date_of_birth,
    }

    for key, value in field_map.items():
        if value is not None:
            data[key] = value

    try:
        return await client.update_contact(contact_id, data)
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def delete_contact(
    contact_id: str,
    ctx: Context | None = None,
) -> dict:
    """Delete a contact permanently.

    Args:
        contact_id: The contact ID to delete
        ctx: MCP context for logging

    Returns:
        Deletion confirmation with succeded flag
    """
    client = await get_client(ctx)
    try:
        return await client.delete_contact(contact_id)
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def upsert_contact(
    location_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    company_name: str | None = None,
    website: str | None = None,
    address1: str | None = None,
    city: str | None = None,
    state: str | None = None,
    postal_code: str | None = None,
    country: str | None = None,
    timezone: str | None = None,
    tags: list[str] | None = None,
    source: str | None = None,
    dnd: bool | None = None,
    assigned_to: str | None = None,
    date_of_birth: str | None = None,
    ctx: Context | None = None,
) -> dict:
    """Create or update a contact based on the location's duplicate detection settings.

    Matching uses the location's "Allow Duplicate Contact" setting to determine
    whether to match by email, phone, or both.

    Args:
        location_id: The location (sub-account) ID (required)
        first_name: First name
        last_name: Last name
        name: Full name
        email: Email address (used for matching)
        phone: Phone number (used for matching)
        company_name: Company name
        website: Website URL
        address1: Street address
        city: City
        state: State
        postal_code: Postal code
        country: Country
        timezone: Timezone
        tags: List of tags
        source: Lead source
        dnd: Do-not-disturb flag
        assigned_to: User ID to assign contact to
        date_of_birth: Date of birth
        ctx: MCP context for logging

    Returns:
        The contact with a 'new' flag indicating if it was created or updated
    """
    client = await get_client(ctx)
    data: dict[str, Any] = {"locationId": location_id}

    field_map = {
        "firstName": first_name,
        "lastName": last_name,
        "name": name,
        "email": email,
        "phone": phone,
        "companyName": company_name,
        "website": website,
        "address1": address1,
        "city": city,
        "state": state,
        "postalCode": postal_code,
        "country": country,
        "timezone": timezone,
        "tags": tags,
        "source": source,
        "dnd": dnd,
        "assignedTo": assigned_to,
        "dateOfBirth": date_of_birth,
    }

    for key, value in field_map.items():
        if value is not None:
            data[key] = value

    try:
        return await client.upsert_contact(data)
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def list_contacts(
    location_id: str,
    query: str | None = None,
    limit: int = 20,
    start_after_id: str | None = None,
    start_after: int | None = None,
    ctx: Context | None = None,
) -> dict:
    """List contacts for a location (deprecated — prefer search_contacts).

    Args:
        location_id: The location (sub-account) ID
        query: Optional search query
        limit: Maximum results (1-100, default 20)
        start_after_id: Cursor for pagination (contact ID)
        start_after: Cursor for pagination (timestamp)
        ctx: MCP context for logging

    Returns:
        List of contacts with count
    """
    client = await get_client(ctx)
    try:
        return await client.list_contacts(
            location_id=location_id,
            query=query,
            limit=limit,
            start_after_id=start_after_id,
            start_after=start_after,
        )
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


@mcp.tool()
async def search_contacts(
    location_id: str,
    query: str | None = None,
    page: int = 1,
    page_limit: int = 20,
    filters: list[dict] | None = None,
    ctx: Context | None = None,
) -> dict:
    """Search contacts with advanced filters.

    Args:
        location_id: The location (sub-account) ID
        query: Free-text search query (searches name, email, phone, etc.)
        page: Page number (default 1)
        page_limit: Results per page (default 20)
        filters: Optional list of filter objects for advanced filtering
        ctx: MCP context for logging

    Returns:
        Search results with contacts
    """
    client = await get_client(ctx)
    data: dict[str, Any] = {"locationId": location_id, "page": page, "pageLimit": page_limit}
    if query:
        data["query"] = query
    if filters:
        data["filters"] = filters

    try:
        return await client.search_contacts(data)
    except GoHighLevelAPIError as e:
        if ctx:
            await ctx.error(f"API error: {e.message}")
        raise


# ============================================================================
# Resources
# ============================================================================


@mcp.resource("skill://gohighlevel/usage")
def skill_usage() -> str:
    """Usage guide for the GoHighLevel MCP server tools."""
    return SKILL_CONTENT


# ============================================================================
# Entrypoints
# ============================================================================

# ASGI app for HTTP deployment (uvicorn mcp_gohighlevel.server:app)
app = mcp.http_app()

# Stdio entrypoint for Claude Desktop / mpak
if __name__ == "__main__":
    logger.info("Running in stdio mode")
    mcp.run()
