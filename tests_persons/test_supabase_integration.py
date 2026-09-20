"""Real PostgreSQL/Supabase verification for the Persons migration.

Run with PERSONS_TEST_DATABASE_URL set to a non-production test connection.
The test deliberately rolls back its transaction and never uses service_role.
"""

import os
from uuid import uuid4

import pytest


psycopg = pytest.importorskip("psycopg")


@pytest.mark.integration
def test_persons_schema_constraints_rls_and_rollback():
    dsn = os.environ.get("PERSONS_TEST_DATABASE_URL")
    if not dsn:
        pytest.skip("PERSONS_TEST_DATABASE_URL is required for real Supabase verification")

    org_a = "integration-org-a"
    org_b = "integration-org-b"
    person_id = uuid4()
    identifier_id = uuid4()
    link_id = uuid4()
    contact_id = uuid4()
    audit_id = uuid4()

    with psycopg.connect(dsn) as connection:
        with connection.transaction():
            with connection.cursor() as cursor:
                cursor.execute("set role authenticated")
                cursor.execute("select set_config('app.organization_id', %s, true)", (org_a,))
                cursor.execute(
                    """
                    select table_name from information_schema.tables
                    where table_schema = 'persons'
                    order by table_name
                    """
                )
                assert [row[0] for row in cursor.fetchall()] == [
                    "person",
                    "person_audit",
                    "person_contact",
                    "person_identifier",
                    "person_organization_link",
                ]

                cursor.execute(
                    """
                    select c.relname, c.relrowsecurity, c.relforcerowsecurity
                    from pg_class c join pg_namespace n on n.oid = c.relnamespace
                    where n.nspname = 'persons' and c.relkind = 'r'
                    order by c.relname
                    """
                )
                assert all(row[1:] == (True, True) for row in cursor.fetchall())

                cursor.execute(
                    """
                    insert into persons.person
                        (organization_id, person_id, display_name, created_by, updated_by)
                    values (%s, %s, 'Integration Person', 'test-user', 'test-user')
                    """,
                    (org_a, person_id),
                )
                cursor.execute(
                    """
                    insert into persons.person_identifier
                        (organization_id, identifier_id, person_id, country_code,
                         document_type, value_original, value_normalized,
                         normalization_version, created_by)
                    values (%s, %s, %s, 'AR', 'national-id', '20-123', '20123', 'v1', 'test-user')
                    """,
                    (org_a, identifier_id, person_id),
                )
                cursor.execute(
                    """
                    insert into persons.person_contact
                        (organization_id, contact_id, person_id, kind,
                         value_original, value_normalized, is_primary)
                    values (%s, %s, %s, 'email', 'a@example.test', 'a@example.test', true)
                    """,
                    (org_a, contact_id, person_id),
                )
                cursor.execute(
                    """
                    insert into persons.person_organization_link
                        (organization_id, link_id, person_id, created_by)
                    values (%s, %s, %s, 'test-user')
                    """,
                    (org_a, link_id, person_id),
                )
                cursor.execute(
                    """
                    insert into persons.person_audit
                        (organization_id, audit_id, person_id, actor_user_id,
                         action, correlation_id, outcome)
                    values (%s, %s, %s, 'test-user', 'person.create', 'corr-1', 'success')
                    """,
                    (org_a, audit_id, person_id),
                )

                cursor.execute("select count(*) from persons.person where organization_id = %s", (org_a,))
                assert cursor.fetchone()[0] == 1
                cursor.execute("select count(*) from persons.person where organization_id = %s", (org_b,))
                assert cursor.fetchone()[0] == 0

                cursor.execute("select set_config('app.organization_id', %s, true)", (org_b,))
                cursor.execute("select count(*) from persons.person")
                assert cursor.fetchone()[0] == 0
                with pytest.raises(psycopg.errors.InsufficientPrivilege):
                    with connection.transaction():
                        cursor.execute(
                            "insert into persons.person (organization_id, person_id, display_name, created_by, updated_by) values (%s, %s, 'cross-tenant', 'u', 'u')",
                            (org_a, uuid4()),
                        )

                cursor.execute("select set_config('app.organization_id', %s, true)", (org_a,))
                with pytest.raises(psycopg.errors.InsufficientPrivilege):
                    with connection.transaction():
                        cursor.execute("update persons.person_audit set outcome = 'tampered'")

        with connection.cursor() as cursor:
            cursor.execute("select count(*) from persons.person where person_id = %s", (person_id,))
            assert cursor.fetchone()[0] == 0
