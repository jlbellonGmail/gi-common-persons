-- Hardening applied after the initial Persons schema deployment.

create or replace function persons.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = timezone('utc', now());
    return new;
end;
$$;

create or replace function persons.reject_audit_mutation()
returns trigger
language plpgsql
as $$
begin
    raise exception 'persons.person_audit is append-only';
end;
$$;

drop trigger if exists person_touch_updated_at on persons.person;
create trigger person_touch_updated_at
before update on persons.person
for each row execute function persons.touch_updated_at();

drop trigger if exists person_contact_touch_updated_at on persons.person_contact;
create trigger person_contact_touch_updated_at
before update on persons.person_contact
for each row execute function persons.touch_updated_at();

drop trigger if exists person_audit_reject_update on persons.person_audit;
create trigger person_audit_reject_update
before update on persons.person_audit
for each row execute function persons.reject_audit_mutation();

drop trigger if exists person_audit_reject_delete on persons.person_audit;
create trigger person_audit_reject_delete
before delete on persons.person_audit
for each row execute function persons.reject_audit_mutation();

revoke update, delete on persons.person_audit from authenticated;
