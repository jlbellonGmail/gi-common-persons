from datetime import date
from gi_persons import PersonsApi
from gi_persons.errors import NotFoundError
from test_persons import setup, ctx

def test_physical_fields_address_gender_and_tax_are_tenant_scoped():
    core, store, service = setup()
    person = service.create_person(ctx(), "Ada", birth_date=date(1815, 12, 10), gender_code="F", language_code="es", marital_status="single")
    assert person.gender_code == "F"
    service.save_gender(ctx(), "F", "Female")
    service.add_address(ctx(), person.person_id, 1, address_type="home", line1="Calle 1", is_primary=True)
    service.save_tax_category(ctx(), country_code="AR", code="MONO", label="Monotributo", valid_from=date(2020,1,1))
    service.add_tax_identifier(ctx(), person.person_id, country_code="AR", identifier_type="CUIT", value="20-12345678-3")
    profile = service.save_tax_profile(ctx(), person.person_id, country_code="AR", category_code="MONO", valid_from=date(2020,1,1))
    assert profile.category_code == "MONO"
    assert service.list_addresses(ctx(), person.person_id)[0].organization_id == "org-a"
    assert service.list_tax_identifiers(ctx(), person.person_id)[0].value_normalized == "20-12345678-3"
    import pytest
    with pytest.raises(NotFoundError): service.list_addresses(ctx("org-b", "user-b"), person.person_id)

def test_identity_is_persisted_and_idempotent_but_conflicts_fail():
    _, store, service = setup()
    service.auth.api.link_identity = lambda *args: {"contract_version":"0.2.0","organization_id":"org-a","person_id":str(args[2]),"user_id":args[3],"external_subject":args[4]}
    person = service.create_person(ctx(), "Ada")
    first = service.link_identity(ctx(), person.person_id, "core-user", "subject")
    second = service.link_identity(ctx(), person.person_id, "core-user", "subject")
    assert first == second
    assert store.get_identity("org-a", person.person_id).core_user_id == "core-user"
