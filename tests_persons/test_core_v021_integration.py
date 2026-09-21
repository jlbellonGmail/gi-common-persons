from uuid import UUID

import pytest

from gi_platform_core import CoreApi, CoreService, InMemoryCoreStore
from gi_persons import IdentifierRules, MemoryStore, PersonsService, RequestContext
from gi_persons.errors import IdentityConflictError, NotFoundError


PERMISSIONS = {
    "persons:read", "persons:write", "persons:identity:read",
    "persons:identity:link", "persons:identity:unlink",
    "organization:identity_link", "organization:identity_unlink",
}


@pytest.fixture
def integrated():
    core_service = CoreService(InMemoryCoreStore())
    core = CoreApi(core_service)
    org = core.create_organization("Persons tenant")
    actor = core.create_user("actor-subject", "Actor")
    target = core.create_user("target-subject", "Target")
    actor_membership = core.add_membership(actor["id"], org["id"])
    core.add_membership(target["id"], org["id"])
    for code in PERMISSIONS:
        core.create_permission(code, code)
    role = core.create_role(org["id"], "persons-admin", PERMISSIONS)
    core.assign_role(actor_membership["id"], role["id"])
    persons = PersonsService(MemoryStore(), core, IdentifierRules())
    context = RequestContext(actor["id"], org["id"])
    return core, persons, context, actor, target, org


def test_public_v021_identity_contract_resolves_and_links_only_opaque_person_id(integrated):
    core, persons, context, actor, target, org = integrated
    person = persons.create_person(context, "Ada")
    resolved = persons.resolve_identity(context, target["id"], target["external_subject"])
    assert resolved["contract_version"] == "0.2.0"

    linked = persons.link_identity(context, person.person_id, target["id"], target["external_subject"])
    assert linked["contract_version"] == "0.2.0"
    assert linked["person_id"] == str(person.person_id)
    assert linked["organization_id"] == org["id"]


def test_link_unlink_are_idempotent_and_audited(integrated):
    _, persons, context, _, target, _ = integrated
    person = persons.create_person(context, "Ada")
    first = persons.link_identity(context, person.person_id, target["id"], target["external_subject"])
    second = persons.link_identity(context, person.person_id, target["id"], target["external_subject"])
    assert first["id"] == second["id"]
    assert persons.unlink_identity(context, person.person_id)["removed"] is True
    assert persons.unlink_identity(context, person.person_id)["removed"] is False
    assert [event.action for event in persons.store.audit].count("identity.link") == 2
    assert [event.action for event in persons.store.audit].count("identity.unlink") == 2


def test_identity_isolation_and_conflicts_fail_closed(integrated):
    core, persons, context, _, target, org = integrated
    person = persons.create_person(context, "Ada")
    other_org = core.create_organization("Other tenant")
    other_user = core.create_user("other-subject", "Other")
    other_membership = core.add_membership(other_user["id"], other_org["id"])
    other_role = core.create_role(other_org["id"], "persons-admin", PERMISSIONS)
    core.assign_role(other_membership["id"], other_role["id"])
    with pytest.raises(NotFoundError):
        persons.resolve_identity(context, other_user["id"], other_user["external_subject"])

    persons.link_identity(context, person.person_id, target["id"], target["external_subject"])
    second_target = core.create_user("second-target-subject", "Second target")
    core.add_membership(second_target["id"], org["id"])
    with pytest.raises(IdentityConflictError):
        persons.link_identity(context, person.person_id, second_target["id"], second_target["external_subject"])


def test_missing_person_is_not_sent_to_core(integrated):
    _, persons, context, _, target, _ = integrated
    missing = UUID("00000000-0000-0000-0000-000000000001")
    with pytest.raises(NotFoundError):
        persons.link_identity(context, missing, target["id"], target["external_subject"])
