from datetime import date
from uuid import uuid4
import pytest

from gi_persons import *
from gi_persons.errors import *

class Core:
    def __init__(self, allowed=True, version="0.1.0", context=True): self.allowed=allowed; self.version=version; self.context=context; self.calls=[]
    def authorize(self,user_id,organization_id,permission,location_id=None):
        self.calls.append((user_id,organization_id,permission,location_id))
        c={"user_id":user_id,"organization_id":organization_id} if self.context else {"user_id":"other","organization_id":organization_id}
        return {"contract_version":self.version,"allowed":self.allowed,"reason":"test","context":c}

def setup():
    core=Core(); rules=IdentifierRules(); rules.register(IdentifierRule("AR","dni","1",strict_alnum))
    store=MemoryStore(); service=PersonsService(store,core,rules); return core,store,service
def ctx(org="org-a",user="user-a"): return RequestContext(user,org)

def test_create_is_authorized_and_json_safe():
    core,store,s=setup(); p=s.create_person(ctx(),"Ada Lovelace",birth_date=date(1815,12,10))
    assert p.organization_id=="org-a" and p.version==1
    assert core.calls[-1][2]=="persons:write"

def test_tenant_isolation_by_id_and_list():
    _,_,s=setup(); p=s.create_person(ctx(),"A")
    assert s.list_persons(ctx("org-b")) == []
    with pytest.raises(NotFoundError): s.get_person(ctx("org-b"),p.person_id)

def test_core_denial_and_malformed_contract_fail_closed():
    core,store,_=setup(); core.allowed=False; s=PersonsService(store,core,IdentifierRules())
    with pytest.raises(ForbiddenError): s.create_person(ctx(),"A")
    core.allowed=True; core.version="9.9.9"
    with pytest.raises(UnsupportedCoreContractError): s.create_person(ctx(),"A")
    core.version="0.1.0"; core.context=False
    with pytest.raises(ForbiddenError): s.create_person(ctx(),"A")

def test_identifier_rule_version_and_tenant_aware_uniqueness():
    _,_,s=setup(); a=s.create_person(ctx(),"A"); b=s.create_person(ctx("org-b","user-b"),"B")
    i=s.add_identifier(ctx(),a.person_id,1,"AR","dni","  ab-12 ")
    assert i.value_original=="  ab-12 " and i.value_normalized=="AB-12" and i.normalization_version=="1"
    s.add_identifier(ctx("org-b","user-b"),b.person_id,1,"AR","dni","AB-12")
    with pytest.raises(DuplicateIdentifierError): s.add_identifier(ctx(),a.person_id,2,"AR","dni","AB-12")

def test_optimistic_concurrency():
    _,_,s=setup(); p=s.create_person(ctx(),"A")
    changed=s.update_person(ctx(),p.person_id,1,display_name="B")
    assert changed.version==2
    with pytest.raises(VersionConflictError): s.update_person(ctx(),p.person_id,1,display_name="C")

def test_contacts_preserve_original_and_primary_is_unique():
    _,store,s=setup(); p=s.create_person(ctx(),"A")
    first=s.add_contact(ctx(),p.person_id,1,"email"," Alice@Example.COM ",is_primary=True)
    second=s.add_contact(ctx(),p.person_id,2,"email","bob@example.com",is_primary=True)
    contacts=s.list_contacts(ctx(),p.person_id)
    assert first.value_original==" Alice@Example.COM "
    assert sum(c.is_primary for c in contacts)==1 and second.is_primary

def test_phone_requires_explicit_country_and_identity_is_disabled():
    _,_,s=setup(); p=s.create_person(ctx(),"A")
    with pytest.raises(ValidationError): s.add_contact(ctx(),p.person_id,1,"phone","5551234")
    with pytest.raises(CapabilityUnavailableError): s.link_identity(ctx(),p.person_id)

def test_duplicate_candidates_are_bounded_and_tenant_scoped():
    _,_,s=setup(); p=s.create_person(ctx(),"Ada Lovelace")
    s.create_person(ctx("org-b","user-b"),"Ada Lovelace")
    candidates=s.find_duplicate_candidates(ctx(),keys=["Ada Lovelace"],limit=1)
    assert len(candidates)==1 and candidates[0][0].person_id==p.person_id

def test_public_api_cursor_is_tenant_and_filter_bound():
    core,store,s=setup(); api=PersonsApi(s,b"secret"); s.create_person(ctx(),"A"); s.create_person(ctx(),"B")
    page=api.list_persons(ctx(),limit=1,filters="status=active")
    assert page["next_cursor"]
    other=api.list_persons(ctx("org-b","user-b"),limit=1,filters="status=active")
    assert other["items"]==[]
    with pytest.raises(ValidationError): api.list_persons(ctx(),limit=1,cursor=page["next_cursor"],filters="status=archived")

def test_errors_are_sanitized():
    err=DuplicateIdentifierError("raw document leaked",details={"value":"PII"})
    assert err.to_json()=={"code":"DUPLICATE_IDENTIFIER","message":"The identifier conflicts within the organization."}

def test_public_facade_masks_identifiers_and_exposes_contacts_and_candidates():
    core,store,s=setup(); api=PersonsApi(s,b"secret"); p=api.create_person(ctx(),display_name="Ada")
    i=api.add_identifier(ctx(),p["person_id"],1,country_code="AR",document_type="dni",value="AB12")
    assert i["value"].endswith("AB12") and i["value"]!="AB12"
    contacts=api.add_contact(ctx(),p["person_id"],2,kind="email",value="a@example.com",is_primary=True)
    assert contacts["kind"]=="email"
    assert api.list_contacts(ctx(),p["person_id"])["items"][0]["value"]=="a@example.com"
    assert api.find_duplicate_candidates(ctx(),keys=["Ada"])["items"][0]["reason"]=="ada"
