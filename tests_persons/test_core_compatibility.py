from gi_persons.authorization import Authorizer
from gi_persons.errors import CoreUnavailableError, ForbiddenError
from gi_persons.models import RequestContext

class PublicCore:
    def authorize(self,*args): return {"contract_version":"0.1.0","allowed":True,"context":{"user_id":args[0],"organization_id":args[1]}}
def test_consumes_only_public_json_shape():
    Authorizer(PublicCore()).require(RequestContext("u","o"),"persons:read")
def test_provider_exception_is_sanitized():
    class Broken:
        def authorize(self,*args): raise RuntimeError("private details")
    try: Authorizer(Broken()).require(RequestContext("u","o"),"persons:read")
    except CoreUnavailableError as error: assert error.to_json()["message"]=="Authorization provider unavailable."
    else: assert False
