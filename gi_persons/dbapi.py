"""Optional DB-API 2.0 adapter; the caller owns the connection and role."""
from contextlib import contextmanager
from uuid import UUID
from .errors import DuplicateIdentifierError, VersionConflictError

class PostgresPersonStore:
    """Small persistence port implementation for PostgreSQL/Supabase.

    It deliberately does not import psycopg or Supabase SDK. A connection
    factory supplied by the host must provide DB-API ``cursor`` and
    transaction semantics. RLS remains the database defense; app settings are
    scoped to one transaction and never interpolated into SQL.
    """
    def __init__(self, connection_factory): self.connection_factory=connection_factory
    @contextmanager
    def transaction(self, organization_id: str, user_id: str):
        connection=self.connection_factory()
        try:
            with connection:
                with connection.cursor() as cur:
                    cur.execute("select set_config('app.organization_id', %s, true)", (organization_id,))
                    cur.execute("select set_config('app.user_id', %s, true)", (user_id,))
                yield connection
        finally: connection.close()
    def insert_person(self, connection, person, link, actor):
        with connection.cursor() as cur:
            cur.execute("""insert into persons.person
              (person_id,organization_id,display_name,given_names,family_names,birth_date,created_by,updated_by)
              values (%s,%s,%s,%s,%s,%s,%s,%s)""", (str(person.person_id),person.organization_id,person.display_name,person.given_names,person.family_names,person.birth_date,actor,actor))
            cur.execute("""insert into persons.person_organization_link
              (link_id,organization_id,person_id,created_by) values (%s,%s,%s,%s)""", (str(link.link_id),link.organization_id,str(link.person_id),actor))
    def insert_identifier(self, connection, identifier, expected_version, actor):
        with connection.cursor() as cur:
            cur.execute("update persons.person set version=version+1,updated_at=timezone('utc',now()),updated_by=%s where organization_id=%s and person_id=%s and version=%s returning version", (actor,identifier.organization_id,str(identifier.person_id),expected_version))
            row=cur.fetchone()
            if row is None: raise VersionConflictError()
            try:
                cur.execute("""insert into persons.person_identifier
                  (identifier_id,organization_id,person_id,country_code,document_type,value_original,value_normalized,normalization_version,created_by)
                  values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (str(identifier.identifier_id),identifier.organization_id,str(identifier.person_id),identifier.country_code,identifier.document_type,identifier.value_original,identifier.value_normalized,identifier.normalization_version,actor))
            except Exception as exc:
                # The host must map the database unique-violation class to this public error.
                if "unique" in str(exc).lower(): raise DuplicateIdentifierError() from exc
                raise
