"""Deterministic, versioned and non-destructive normalization."""
import re
from dataclasses import dataclass
from typing import Callable
from .errors import ValidationError

@dataclass(frozen=True, slots=True)
class IdentifierRule:
    country_code: str
    document_type: str
    version: str
    normalize: Callable[[str], str]

class IdentifierRules:
    def __init__(self): self._rules: dict[tuple[str, str], IdentifierRule] = {}
    def register(self, rule: IdentifierRule) -> None:
        key = (rule.country_code.upper(), rule.document_type)
        if not rule.version or not callable(rule.normalize): raise ValueError("invalid identifier rule")
        self._rules[key] = rule
    def normalize(self, country_code: str, document_type: str, value: str) -> tuple[str, str]:
        key = (country_code.upper(), document_type)
        rule = self._rules.get(key)
        if rule is None: raise ValidationError("unsupported identifier type")
        if not isinstance(value, str) or not value.strip(): raise ValidationError("identifier value is required")
        normalized = rule.normalize(value)
        if not normalized: raise ValidationError("identifier value is invalid")
        return normalized, rule.version

def strict_alnum(value: str) -> str:
    value = value.strip().upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9 ./-]*", value): raise ValidationError("identifier value is invalid")
    return value

def normalize_email(value: str) -> str:
    if not isinstance(value, str): raise ValidationError("email is invalid")
    original = value.strip()
    if original.count("@") != 1: raise ValidationError("email is invalid")
    local, domain = original.rsplit("@", 1)
    if not local or not domain or any(c.isspace() for c in original): raise ValidationError("email is invalid")
    return f"{local}@{domain.casefold()}"

def normalize_phone(value: str) -> str:
    if not isinstance(value, str): raise ValidationError("phone is invalid")
    compact = re.sub(r"[ ()-]", "", value.strip())
    if not re.fullmatch(r"\+[1-9][0-9]{7,14}", compact): raise ValidationError("phone requires explicit E.164 country prefix")
    return compact

def name_key(value: str) -> str:
    return " ".join(value.split()).casefold()
