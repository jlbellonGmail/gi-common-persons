-- GI Persons tenant-aware schema.
-- The application role must set LOCAL app.organization_id in each transaction.

create extension if not exists pgcrypto;
create schema if not exists persons;

create table if not exists persons.person (
    organization_id text not null,
    person_id uuid not null default gen_random_uuid(),
    display_name text not null check (length(btrim(display_name)) between 1 and 200),
    given_names text,
    family_names text,
    birth_date date,
    status text not null default 'active' check (status in ('active', 'archived')),
    version bigint not null default 1 check (version > 0),
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now()),
    created_by text not null,
    updated_by text not null,
    primary key (organization_id, person_id)
);

create table if not exists persons.person_identifier (
    organization_id text not null,
    identifier_id uuid not null default gen_random_uuid(),
    person_id uuid not null,
    country_code text not null check (country_code ~ '^[A-Z]{2}$'),
    document_type text not null check (length(btrim(document_type)) between 1 and 80),
    value_original text not null,
    value_normalized text not null,
    normalization_version text not null,
    created_at timestamptz not null default timezone('utc', now()),
    created_by text not null,
    primary key (organization_id, identifier_id),
    foreign key (organization_id, person_id)
        references persons.person (organization_id, person_id) on delete restrict,
    unique (organization_id, country_code, document_type, value_normalized)
);

create table if not exists persons.person_contact (
    organization_id text not null,
    contact_id uuid not null default gen_random_uuid(),
    person_id uuid not null,
    kind text not null check (kind in ('email', 'phone')),
    value_original text not null,
    value_normalized text not null,
    label text,
    is_primary boolean not null default false,
    verified_at timestamptz,
    created_at timestamptz not null default timezone('utc', now()),
    updated_at timestamptz not null default timezone('utc', now()),
    primary key (organization_id, contact_id),
    foreign key (organization_id, person_id)
        references persons.person (organization_id, person_id) on delete restrict
);

create table if not exists persons.person_organization_link (
    organization_id text not null,
    link_id uuid not null default gen_random_uuid(),
    person_id uuid not null,
    link_status text not null default 'active' check (link_status in ('active', 'inactive')),
    created_at timestamptz not null default timezone('utc', now()),
    created_by text not null,
    primary key (organization_id, link_id),
    foreign key (organization_id, person_id)
        references persons.person (organization_id, person_id) on delete restrict,
    unique (organization_id, person_id)
);

create table if not exists persons.person_audit (
    organization_id text not null,
    audit_id uuid not null default gen_random_uuid(),
    person_id uuid not null,
    actor_user_id text not null,
    action text not null,
    occurred_at timestamptz not null default timezone('utc', now()),
    correlation_id text not null,
    outcome text not null,
    entity_version bigint,
    primary key (organization_id, audit_id),
    foreign key (organization_id, person_id)
        references persons.person (organization_id, person_id) on delete restrict
);

create unique index if not exists person_contact_primary_per_kind
    on persons.person_contact (organization_id, person_id, kind) where is_primary;
create index if not exists person_by_organization_status
    on persons.person (organization_id, status, person_id);
create index if not exists person_identifier_by_person
    on persons.person_identifier (organization_id, person_id);
create index if not exists person_contact_by_person
    on persons.person_contact (organization_id, person_id);
create index if not exists person_link_by_person
    on persons.person_organization_link (organization_id, person_id);
create index if not exists person_audit_by_person_time
    on persons.person_audit (organization_id, person_id, occurred_at desc);

grant usage on schema persons to authenticated;
grant select, insert, update on persons.person to authenticated;
grant select, insert on persons.person_identifier to authenticated;
grant select, insert, update on persons.person_contact to authenticated;
grant select, insert, update on persons.person_organization_link to authenticated;
grant select, insert on persons.person_audit to authenticated;

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

create trigger person_touch_updated_at
before update on persons.person
for each row execute function persons.touch_updated_at();

create trigger person_contact_touch_updated_at
before update on persons.person_contact
for each row execute function persons.touch_updated_at();

create trigger person_audit_reject_update
before update on persons.person_audit
for each row execute function persons.reject_audit_mutation();

create trigger person_audit_reject_delete
before delete on persons.person_audit
for each row execute function persons.reject_audit_mutation();

revoke update, delete on persons.person_audit from authenticated;

do $$
declare table_name text;
begin
    foreach table_name in array array['person', 'person_identifier', 'person_contact', 'person_organization_link', 'person_audit'] loop
        execute format('alter table persons.%I enable row level security', table_name);
        execute format('alter table persons.%I force row level security', table_name);
        execute format('drop policy if exists persons_tenant_select on persons.%I', table_name);
        execute format('drop policy if exists persons_tenant_insert on persons.%I', table_name);
        execute format('drop policy if exists persons_tenant_update on persons.%I', table_name);
        execute format('create policy persons_tenant_select on persons.%I for select using (organization_id = current_setting(''app.organization_id'', true))', table_name);
        execute format('create policy persons_tenant_insert on persons.%I for insert with check (organization_id = current_setting(''app.organization_id'', true))', table_name);
        execute format('create policy persons_tenant_update on persons.%I for update using (organization_id = current_setting(''app.organization_id'', true)) with check (organization_id = current_setting(''app.organization_id'', true))', table_name);
    end loop;
end $$;

comment on schema persons is 'Tenant-aware common Persons data; organization_id is the isolation boundary.';
