"""Pydantic models for GoHighLevel API responses."""

from typing import Any

from pydantic import BaseModel, Field


class DndSettingsEntry(BaseModel):
    """A single DND channel setting."""

    model_config = {"populate_by_name": True}

    status: str | None = Field(None, description="DND status (active/inactive)")
    message: str | None = Field(None, description="DND message")
    code: str | None = Field(None, description="DND code")


class DndSettings(BaseModel):
    """Do-not-disturb settings per channel."""

    model_config = {"populate_by_name": True}

    call: DndSettingsEntry | None = Field(None, alias="Call")
    email: DndSettingsEntry | None = Field(None, alias="Email")
    sms: DndSettingsEntry | None = Field(None, alias="SMS")
    whatsapp: DndSettingsEntry | None = Field(None, alias="WhatsApp")
    gm_b: DndSettingsEntry | None = Field(None, alias="GMB")
    fb: DndSettingsEntry | None = Field(None, alias="FB")


class Contact(BaseModel):
    """A contact from the GoHighLevel API."""

    model_config = {"populate_by_name": True}

    id: str = Field(..., description="Contact ID")
    first_name: str | None = Field(None, alias="firstName", description="First name")
    last_name: str | None = Field(None, alias="lastName", description="Last name")
    name: str | None = Field(None, description="Full name")
    email: str | None = Field(None, description="Email address")
    phone: str | None = Field(None, description="Phone number")
    location_id: str | None = Field(None, alias="locationId", description="Location ID")
    company_name: str | None = Field(None, alias="companyName", description="Company name")
    website: str | None = Field(None, description="Website URL")
    address1: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City")
    state: str | None = Field(None, description="State")
    postal_code: str | None = Field(None, alias="postalCode", description="Postal code")
    country: str | None = Field(None, description="Country")
    timezone: str | None = Field(None, description="Timezone")
    tags: list[str] | None = Field(None, description="Tags")
    source: str | None = Field(None, description="Lead source")
    dnd: bool | None = Field(None, description="Global DND flag")
    dnd_settings: DndSettings | None = Field(
        None, alias="dndSettings", description="Per-channel DND"
    )
    custom_fields: list[dict[str, Any]] | None = Field(
        None, alias="customFields", description="Custom field values"
    )
    date_added: str | None = Field(None, alias="dateAdded", description="Created timestamp")
    date_updated: str | None = Field(None, alias="dateUpdated", description="Updated timestamp")
    date_of_birth: str | None = Field(None, alias="dateOfBirth", description="Date of birth")
    assigned_to: str | None = Field(None, alias="assignedTo", description="Assigned user ID")


class ContactResponse(BaseModel):
    """Response wrapping a single contact."""

    contact: Contact


class ContactListResponse(BaseModel):
    """Response for listing contacts."""

    contacts: list[Contact] = Field(default_factory=list)
    count: int | None = Field(None, description="Total count")


class UpdateContactResponse(BaseModel):
    """Response for updating a contact."""

    succeded: bool = Field(default=False, description="Whether the update succeeded (GHL typo)")
    contact: Contact | None = None


class DeleteContactResponse(BaseModel):
    """Response for deleting a contact."""

    succeded: bool = Field(default=False, description="Whether the delete succeeded (GHL typo)")


class UpsertContactResponse(BaseModel):
    """Response for upserting a contact."""

    model_config = {"populate_by_name": True}

    new: bool = Field(default=False, description="True if created, False if updated")
    contact: Contact
    trace_id: str | None = Field(None, alias="traceId", description="Trace ID")
