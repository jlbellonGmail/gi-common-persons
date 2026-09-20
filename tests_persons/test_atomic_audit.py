import pytest
from gi_persons import IdentifierRules, MemoryStore, PersonsService, RequestContext
from gi_persons.errors import AuditFailureError

class Core:
    def authorize(self,u,o,p,l=None): return {"contract_version":"0.1.0","allowed":True,"context":{"user_id":u,"organization_id":o}}
class FailingAudit:
    def append(self,event): raise RuntimeError("sink down")

def test_audit_failure_rolls_back_mutation():
    store=MemoryStore(); service=PersonsService(store,Core(),IdentifierRules(),audit_sink=FailingAudit())
    with pytest.raises(AuditFailureError): service.create_person(RequestContext("u","o"),"A")
    assert store.list_persons("o",10)==[]
