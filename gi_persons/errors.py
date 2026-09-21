"""Public, transport-neutral Persons errors."""

class PersonsError(Exception):
    code = "PERSONS_ERROR"
    safe_message = "Persons operation failed."

    def __init__(self, message: str | None = None, *, details: dict | None = None):
        super().__init__(message or self.safe_message)
        self.details = details or {}

    def to_json(self) -> dict:
        return {"code": self.code, "message": self.safe_message}

class ValidationError(PersonsError):
    code = "VALIDATION_ERROR"; safe_message = "The request is invalid."
class NotFoundError(PersonsError):
    code = "NOT_FOUND"; safe_message = "The requested resource was not found."
class ForbiddenError(PersonsError):
    code = "FORBIDDEN"; safe_message = "The operation is not permitted."
class CoreUnavailableError(PersonsError):
    code = "CORE_UNAVAILABLE"; safe_message = "Authorization provider unavailable."
class UnsupportedCoreContractError(PersonsError):
    code = "UNSUPPORTED_CORE_CONTRACT"; safe_message = "Authorization contract unsupported."
class DuplicateIdentifierError(PersonsError):
    code = "DUPLICATE_IDENTIFIER"; safe_message = "The identifier conflicts within the organization."
class VersionConflictError(PersonsError):
    code = "VERSION_CONFLICT"; safe_message = "The resource changed; refresh and retry."
class CapabilityUnavailableError(PersonsError):
    code = "CAPABILITY_UNAVAILABLE"; safe_message = "This capability is not available."
class AuditFailureError(PersonsError):
    code = "AUDIT_UNAVAILABLE"; safe_message = "The operation could not be safely recorded."
class IdentityConflictError(PersonsError):
    code = "IDENTITY_CONFLICT"; safe_message = "The identity conflicts within the organization."
