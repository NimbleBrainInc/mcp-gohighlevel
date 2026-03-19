# GoHighLevel MCP Server — Skill Guide

## Tools

| Tool | Use when... |
|------|-------------|
| `get_contact` | You have a contact ID and need full details |
| `create_contact` | You need to create a new contact (requires locationId) |
| `update_contact` | You need to modify specific fields on an existing contact |
| `delete_contact` | You need to remove a contact permanently |
| `upsert_contact` | You want to create-or-update based on email/phone matching |
| `list_contacts` | You need a simple paginated list (deprecated — prefer search) |
| `search_contacts` | You need to find contacts with filters or free-text search |

## Context Reuse

- Use the `id` from `create_contact` or `upsert_contact` response for follow-up `get_contact` or `update_contact` calls
- Use `contact.id` values from `list_contacts` or `search_contacts` results when calling `get_contact`, `update_contact`, or `delete_contact`
- The `upsert_contact` response includes a `new` boolean — use it to determine if the contact was created or updated
- All write operations require a `locationId` — get this from an existing contact or the user

## Important Notes

- **Tags on update overwrite**: `update_contact` with tags replaces ALL existing tags. For add/remove, use the GHL Tags API directly.
- **Upsert matching**: Uses the location's "Allow Duplicate Contact" setting to match by email/phone priority.
- **list_contacts is deprecated**: GHL recommends `search_contacts` instead.

## Workflows

### 1. Find and Update a Contact
1. `search_contacts` with location_id and query (name, email, or phone)
2. `get_contact` with the matching contact's ID for full details
3. `update_contact` with only the fields that need changing

### 2. Import / Sync a Contact
1. `upsert_contact` with location_id, email, and/or phone plus all known fields
2. Check response `new` field to confirm create vs. update
3. `get_contact` with returned ID to verify final state

### 3. Bulk Lookup
1. `search_contacts` with location_id and filters (e.g., by tag or date range)
2. For each contact needing detail: `get_contact` with the ID
3. Summarize findings
