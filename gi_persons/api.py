"""Versioned JSON-safe facade without HTTP assumptions."""
import base64, hashlib, hmac, json
from dataclasses import asdict
from uuid import UUID
from .errors import PersonsError, ValidationError
from .models import RequestContext, json_value

class CursorCodec:
    def __init__(self, secret: bytes):
        if not secret: raise ValueError("cursor secret required")
        self.secret=secret
    def encode(self, org, filters, last_id):
        payload=json.dumps({"o":org,"f":filters,"l":str(last_id)},sort_keys=True,separators=(",",":" )).encode()
        sig=hmac.new(self.secret,payload,hashlib.sha256).digest()
        return base64.urlsafe_b64encode(payload+b"."+sig).decode().rstrip("=")
    def decode(self, org, filters, token):
        try:
            raw=base64.urlsafe_b64decode(token+"="*((4-len(token)%4)%4)); payload,sig=raw.rsplit(b".",1)
            if not hmac.compare_digest(sig,hmac.new(self.secret,payload,hashlib.sha256).digest()): raise ValueError
            data=json.loads(payload)
            if data["o"]!=org or data["f"]!=filters: raise ValueError
            return UUID(data["l"])
        except Exception as exc: raise ValidationError() from exc

def summary(person):
    return json_value({"contract_version":"0.1.0","organization_id":person.organization_id,"person_id":person.person_id,"display_name":person.display_name,"given_names":person.given_names,"family_names":person.family_names,"birth_date":person.birth_date,"status":person.status,"version":person.version,"created_at":person.created_at,"updated_at":person.updated_at})

def public_identifier(identifier, reveal=False):
    value=identifier.value_original if reveal else "*" * max(4, len(identifier.value_normalized)-4) + identifier.value_normalized[-4:]
    return json_value({"contract_version":"0.1.0","identifier_id":identifier.identifier_id,"organization_id":identifier.organization_id,"person_id":identifier.person_id,"country_code":identifier.country_code,"document_type":identifier.document_type,"value":value,"normalization_version":identifier.normalization_version})

def public_contact(contact):
    return json_value({"contract_version":"0.1.0","contact_id":contact.contact_id,"organization_id":contact.organization_id,"person_id":contact.person_id,"kind":contact.kind,"value":contact.value_normalized,"label":contact.label,"is_primary":contact.is_primary,"verified_at":contact.verified_at})

# Keep the summary contract JSON-safe while exposing the optional physical-person fields.
def summary(person):
    return json_value({"contract_version":"0.1.0","organization_id":person.organization_id,"person_id":person.person_id,
        "display_name":person.display_name,"given_names":person.given_names,"family_names":person.family_names,
        "birth_date":person.birth_date,"gender_code":person.gender_code,"language_code":person.language_code,
        "marital_status":person.marital_status,"death_date":person.death_date,"status":person.status,
        "version":person.version,"created_at":person.created_at,"updated_at":person.updated_at})

class PersonsApi:
    def __init__(self, service, cursor_secret: bytes): self.service=service; self.cursors=CursorCodec(cursor_secret)
    def create_person(self, context: RequestContext, **data): return summary(self.service.create_person(context,**data))
    def get_person(self, context, person_id): return summary(self.service.get_person(context,UUID(str(person_id))))
    def list_persons(self, context, *, limit=20, cursor=None, filters=""):
        after=self.cursors.decode(context.organization_id,filters,cursor) if cursor else None
        items=self.service.list_persons(context,limit+1,after); more=len(items)>limit; items=items[:limit]
        return {"contract_version":"0.1.0","items":[summary(p) for p in items],"next_cursor":self.cursors.encode(context.organization_id,filters,items[-1].person_id) if more and items else None}
    def add_identifier(self, context, person_id, expected_version, **data):
        return public_identifier(self.service.add_identifier(context,UUID(str(person_id)),expected_version,**data))
    def list_identifiers(self, context, person_id, *, reveal=False):
        if reveal:
            self.service.auth.require(context,"persons:identifier:reveal")
        return {"contract_version":"0.1.0","items":[public_identifier(i,reveal) for i in self.service.list_identifiers(context,UUID(str(person_id)))]}
    def add_contact(self, context, person_id, expected_version, **data):
        return public_contact(self.service.add_contact(context,UUID(str(person_id)),expected_version,**data))
    def list_contacts(self, context, person_id):
        return {"contract_version":"0.1.0","items":[public_contact(c) for c in self.service.list_contacts(context,UUID(str(person_id)))]}
    def find_duplicate_candidates(self, context, *, keys, limit=20):
        items=self.service.find_duplicate_candidates(context,keys=keys,limit=limit)
        return {"contract_version":"0.1.0","items":[{"person_id":str(p.person_id),"organization_id":p.organization_id,"reason":reason} for p,reason in items]}
    def resolve_identity(self, context, user_id, external_subject):
        return self.service.resolve_identity(context, str(user_id), external_subject)
    def link_identity(self, context, person_id, user_id, external_subject):
        return self.service.link_identity(context, UUID(str(person_id)), str(user_id), external_subject)
    def unlink_identity(self, context, person_id):
        return self.service.unlink_identity(context, UUID(str(person_id)))
    def add_address(self, context, person_id, expected_version, **data):
        return json_value(self.service.add_address(context, UUID(str(person_id)), expected_version, **data))
    def list_addresses(self, context, person_id):
        return {"contract_version":"0.1.0","items":[json_value(a) for a in self.service.list_addresses(context,UUID(str(person_id)))]}
    def list_genders(self, context): return {"contract_version":"0.1.0","items":[json_value(g) for g in self.service.list_genders(context)]}
    def save_gender(self, context, code, label, *, active=True): return json_value(self.service.save_gender(context,code,label,active=active))
    def get_identity(self, context, person_id): return json_value(self.service.get_identity(context,UUID(str(person_id))))
    def add_tax_identifier(self, context, person_id, **data): return json_value(self.service.add_tax_identifier(context,UUID(str(person_id)),**data))
    def list_tax_identifiers(self, context, person_id): return {"contract_version":"0.1.0","items":[json_value(i) for i in self.service.list_tax_identifiers(context,UUID(str(person_id)))]}
    def error(self, exc: Exception): return exc.to_json() if isinstance(exc,PersonsError) else {"code":"INTERNAL_ERROR","message":"Persons operation failed."}
