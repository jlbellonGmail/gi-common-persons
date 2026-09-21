"""Application use cases; every operation authorizes before tenant access."""
from dataclasses import replace
from uuid import UUID, uuid4
from .authorization import Authorizer, SUPPORTED_IDENTITY_CONTRACT
from .errors import *
from .models import *
from .normalization import *
from contextlib import nullcontext

class PersonsService:
    def __init__(self, store, core_api, identifier_rules: IdentifierRules, audit_sink=None):
        self.store=store; self.auth=Authorizer(core_api); self.rules=identifier_rules; self.audit_sink=audit_sink
    def _audit(self, ctx, person_id, action, outcome, version):
        event=AuditEvent(uuid4(),ctx.organization_id,person_id,ctx.user_id,action,utcnow(),ctx.correlation_id,outcome,version)
        try:
            if self.audit_sink: self.audit_sink.append(event)
            elif hasattr(self.store,"_event"): self.store._event(event)
        except Exception as exc: raise AuditFailureError() from exc
    def _transaction(self):
        return self.store.transaction() if hasattr(self.store,"transaction") else nullcontext()
    def create_person(self, ctx, display_name, *, given_names=None, family_names=None, birth_date=None):
        self.auth.require(ctx,"persons:write")
        if not isinstance(display_name,str) or not display_name.strip() or len(display_name)>200: raise ValidationError()
        if birth_date and birth_date > date.today(): raise ValidationError()
        p=Person(uuid4(),ctx.organization_id,display_name.strip(),given_names,family_names,birth_date)
        link=OrganizationLink(uuid4(),ctx.organization_id,p.person_id)
        with self._transaction():
            result=self.store.create_person(p,link); self._audit(ctx,p.person_id,"person.create","success",result.version); return result
    def get_person(self, ctx, person_id):
        self.auth.require(ctx,"persons:read"); p=self.store.get_person(ctx.organization_id,person_id)
        if p is None: raise NotFoundError()
        return p
    def list_persons(self, ctx, limit=20, after=None):
        self.auth.require(ctx,"persons:read")
        if limit<1 or limit>101: raise ValidationError()
        return self.store.list_persons(ctx.organization_id,limit,after)
    def update_person(self, ctx, person_id, expected_version, **fields):
        self.auth.require(ctx,"persons:write"); current=self.get_person(ctx,person_id)
        allowed={"display_name","given_names","family_names","birth_date"}
        if set(fields)-allowed: raise ValidationError()
        if "display_name" in fields and (not fields["display_name"] or len(fields["display_name"])>200): raise ValidationError()
        if fields.get("birth_date") and fields["birth_date"]>date.today(): raise ValidationError()
        updated=replace(current,**fields)
        with self._transaction():
            result=self.store.update_person(updated,expected_version)
            self._audit(ctx,person_id,"person.update","success",result.version); return result
    def add_identifier(self, ctx, person_id, expected_version, country_code, document_type, value):
        self.auth.require(ctx,"persons:identifier:write"); self.get_person(ctx,person_id)
        code=country_code.upper()
        if len(code)!=2 or not code.isalpha(): raise ValidationError()
        normalized,version=self.rules.normalize(code,document_type,value)
        i=Identifier(uuid4(),ctx.organization_id,person_id,code,document_type,value,normalized,version)
        with self._transaction():
            result=self.store.add_identifier(i,expected_version); self._audit(ctx,person_id,"identifier.add","success",expected_version+1); return result
    def list_identifiers(self, ctx, person_id):
        self.auth.require(ctx,"persons:identifier:read"); self.get_person(ctx,person_id); return self.store.list_identifiers(ctx.organization_id,person_id)
    def add_contact(self, ctx, person_id, expected_version, kind, value, *, label=None, is_primary=False):
        self.auth.require(ctx,"persons:contact:write"); self.get_person(ctx,person_id)
        if kind not in {"email","phone"}: raise ValidationError()
        normalized=normalize_email(value) if kind=="email" else normalize_phone(value)
        c=Contact(uuid4(),ctx.organization_id,person_id,kind,value,normalized,label,is_primary)
        with self._transaction():
            result=self.store.add_contact(c,expected_version); self._audit(ctx,person_id,"contact.add","success",expected_version+1); return result
    def list_contacts(self, ctx, person_id):
        self.auth.require(ctx,"persons:contact:read"); self.get_person(ctx,person_id); return self.store.list_contacts(ctx.organization_id,person_id)
    def find_duplicate_candidates(self, ctx, *, keys, limit=20):
        self.auth.require(ctx,"persons:duplicates:read")
        if limit<1 or limit>100: raise ValidationError()
        safe={name_key(k) for k in keys if isinstance(k,str) and k.strip()}
        return self.store.candidates(ctx.organization_id,safe,limit)
    def _core_identity_call(self, operation):
        try:
            response = operation()
        except Exception as exc:
            name = type(exc).__name__.lower()
            if "conflict" in name:
                raise IdentityConflictError() from exc
            if "authorization" in name or "isolation" in name or "forbidden" in name:
                raise ForbiddenError() from exc
            if "notfound" in name or "not_found" in name:
                raise NotFoundError() from exc
            raise CoreUnavailableError() from exc
        if not isinstance(response, dict) or response.get("contract_version") != SUPPORTED_IDENTITY_CONTRACT:
            raise UnsupportedCoreContractError()
        return response

    def resolve_identity(self, ctx, user_id, external_subject):
        """Resolve a Core identity inside the request tenant only."""
        self.auth.require(ctx, "persons:identity:read")
        response = self._core_identity_call(
            lambda: self.auth.api.validate_identity(ctx.organization_id, str(user_id), external_subject),
        )
        if response.get("organization_id") != ctx.organization_id or response.get("valid") is not True:
            raise ForbiddenError()
        user = response.get("user")
        if not isinstance(user, dict) or user.get("id") != str(user_id):
            raise ForbiddenError()
        return response

    def link_identity(self, ctx, person_id, user_id, external_subject):
        self.auth.require(ctx, "persons:identity:link")
        self.get_person(ctx, person_id)
        # Core receives only the opaque reference. The Person aggregate never crosses this boundary.
        response = self._core_identity_call(
            lambda: self.auth.api.link_identity(ctx.user_id, ctx.organization_id, str(person_id), str(user_id), external_subject),
        )
        with self._transaction():
            self._audit(ctx, person_id, "identity.link", "success", None)
        return response

    def unlink_identity(self, ctx, person_id):
        self.auth.require(ctx, "persons:identity:unlink")
        self.get_person(ctx, person_id)
        response = self._core_identity_call(
            lambda: self.auth.api.unlink_identity(ctx.user_id, ctx.organization_id, str(person_id)),
        )
        with self._transaction():
            outcome = "success" if response.get("removed") is True else "success_idempotent"
            self._audit(ctx, person_id, "identity.unlink", outcome, None)
        return response
