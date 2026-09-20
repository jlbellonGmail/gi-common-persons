do $$
declare
    pid uuid := gen_random_uuid();
    duplicate_pid uuid := gen_random_uuid();
    seen integer;
begin
    execute 'set local role authenticated';
    perform set_config('app.organization_id', 'unit-a', true);

    begin
        insert into persons.person (organization_id, person_id, display_name, created_by, updated_by)
        values ('unit-a', pid, 'Integration A', 'test-user', 'test-user');
        insert into persons.person_identifier
            (organization_id, identifier_id, person_id, country_code, document_type,
             value_original, value_normalized, normalization_version, created_by)
        values ('unit-a', gen_random_uuid(), pid, 'AR', 'national-id', '20-123', '20123', 'v1', 'test-user');
        begin
            insert into persons.person_identifier
                (organization_id, identifier_id, person_id, country_code, document_type,
                 value_original, value_normalized, normalization_version, created_by)
            values ('unit-a', gen_random_uuid(), pid, 'AR', 'national-id', '20-123', '20123', 'v1', 'test-user');
            raise exception 'duplicate identifier was accepted';
        exception when unique_violation then
            null;
        end;
        insert into persons.person_contact
            (organization_id, contact_id, person_id, kind, value_original, value_normalized, is_primary)
        values ('unit-a', gen_random_uuid(), pid, 'email', 'a@example.test', 'a@example.test', true);
        begin
            insert into persons.person_contact
                (organization_id, contact_id, person_id, kind, value_original, value_normalized, is_primary)
            values ('unit-a', gen_random_uuid(), pid, 'email', 'b@example.test', 'b@example.test', true);
            raise exception 'duplicate primary contact was accepted';
        exception when unique_violation then
            null;
        end;
        insert into persons.person_audit
            (organization_id, audit_id, person_id, actor_user_id, action, correlation_id, outcome)
        values ('unit-a', gen_random_uuid(), pid, 'test-user', 'person.create', 'integration-1', 'success');
        begin
            update persons.person_audit set outcome = 'tampered' where person_id = pid;
            raise exception 'audit update was accepted';
        exception when insufficient_privilege then
            null;
        end;

        perform set_config('app.organization_id', 'unit-b', true);
        select count(*) into seen from persons.person where person_id = pid;
        if seen <> 0 then raise exception 'tenant B read tenant A data'; end if;
        begin
            insert into persons.person (organization_id, person_id, display_name, created_by, updated_by)
            values ('unit-a', duplicate_pid, 'Cross tenant write', 'test-user', 'test-user');
            raise exception 'tenant B wrote tenant A data';
        exception when insufficient_privilege then
            null;
        end;
        perform set_config('app.organization_id', 'unit-a', true);
        raise exception using errcode = 'P0001', message = 'rollback sentinel';
    exception when sqlstate 'P0001' then
        null;
    end;

    perform set_config('app.organization_id', 'unit-a', true);
    select count(*) into seen from persons.person where person_id = pid;
    if seen <> 0 then raise exception 'rollback did not remove integration rows'; end if;
    raise notice 'PASS schema, unique constraints, tenant RLS, audit immutability and rollback';
end $$;
