"""Domain values and trusted request context."""
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Any
from uuid import UUID, uuid4

def utcnow() -> datetime: return datetime.now(timezone.utc)

@dataclass(frozen=True, slots=True)
class RequestContext:
    user_id: str
    organization_id: str
    location_id: str | None = None
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    trusted: bool = True
    def __post_init__(self):
        if not self.trusted or not self.user_id or not self.organization_id:
            raise ValueError("context must be trusted and identify user and organization")

@dataclass(frozen=True, slots=True)
class Person:
    person_id: UUID
    organization_id: str
    display_name: str
    given_names: str | None = None
    family_names: str | None = None
    birth_date: date | None = None
    status: str = "active"
    version: int = 1
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

@dataclass(frozen=True, slots=True)
class Identifier:
    identifier_id: UUID
    organization_id: str
    person_id: UUID
    country_code: str
    document_type: str
    value_original: str
    value_normalized: str
    normalization_version: str
    created_at: datetime = field(default_factory=utcnow)

@dataclass(frozen=True, slots=True)
class Contact:
    contact_id: UUID
    organization_id: str
    person_id: UUID
    kind: str
    value_original: str
    value_normalized: str
    label: str | None = None
    is_primary: bool = False
    verified_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

@dataclass(frozen=True, slots=True)
class OrganizationLink:
    link_id: UUID
    organization_id: str
    person_id: UUID
    status: str = "active"
    created_at: datetime = field(default_factory=utcnow)

@dataclass(frozen=True, slots=True)
class AuditEvent:
    audit_id: UUID
    organization_id: str
    person_id: UUID | None
    actor_user_id: str
    action: str
    occurred_at: datetime
    correlation_id: str
    outcome: str
    entity_version: int | None

def json_value(value: Any) -> Any:
    if isinstance(value, UUID): return str(value)
    if isinstance(value, (datetime, date)): return value.isoformat()
    if isinstance(value, dict): return {str(k): json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [json_value(v) for v in value]
    return value
