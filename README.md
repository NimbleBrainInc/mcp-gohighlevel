# GoHighLevel MCP Server

An MCP (Model Context Protocol) server for managing contacts in GoHighLevel CRM. Supports full CRUD, upsert, list, and search operations.

## Features

- Get, create, update, delete contacts
- Upsert contacts with duplicate detection
- List and search contacts with filters
- Async HTTP client with error handling
- Typed responses with Pydantic models

## Installation

### Using mpak (Recommended)

```bash
# Configure your API key
mpak config set @nimblebraininc/gohighlevel api_key=your_api_key_here

# Run the server
mpak run @nimblebraininc/gohighlevel
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/NimbleBrainInc/mcp-gohighlevel.git
cd mcp-gohighlevel

# Install dependencies with uv
uv sync

# Set your API key
export GOHIGHLEVEL_API_KEY=your_api_key_here

# Run the server
uv run python -m mcp_gohighlevel.server
```

## Configuration

### Getting Your API Key

Use a **Private Integration Token** or **OAuth Access Token** from your GoHighLevel account. See the [GoHighLevel API docs](https://marketplace.gohighlevel.com/docs/Authorization/authorization_doc) for setup instructions.

### Claude Desktop Configuration

Add to your `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "gohighlevel": {
      "command": "mpak",
      "args": ["run", "@nimblebraininc/gohighlevel"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_contact` | Get a single contact by ID |
| `create_contact` | Create a new contact |
| `update_contact` | Update an existing contact |
| `delete_contact` | Delete a contact by ID |
| `upsert_contact` | Create or update a contact based on duplicate settings |
| `list_contacts` | List contacts for a location (deprecated) |
| `search_contacts` | Search contacts with advanced filters |

## Development

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest tests/ -v

# Format code
uv run ruff format src/ tests/

# Lint
uv run ruff check src/ tests/

# Type check
uv run ty check src/

# Run all checks
make check
```

## License

MIT
