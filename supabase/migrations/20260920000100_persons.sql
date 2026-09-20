-- GI Persons schema. Execute with a tenant-bound application role.
-- The host must SET LOCAL app.organization_id and app.user_id per transaction.
create extension if not exists pgcrypto;

create table if not exists public.persons (
  person_id uuid primary key default gen_random_uuid(),
  organization_id text not null,
  display_name text not null check (length(btrim(display_name)) between 1 and 200),
  given_names text,
  family_names text,
  birth_date date check (birth_date is null or birth_date <= current_date),
  status text not null default 'active' check (status in ('active','archived')),
  version bigint not null default 1 check (version > 0),
  created_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now()),
  created_by text not null,
  updated_by text not null,
  unique (organization_id, person_id)
);

create table if not exists public.person_identifiers (
  identifier_id uuid primary key default gen_random_uuid(),
  organization_id text not null,
  person_id uuid not null,
  country_code text not null check (country_code ~ '^[A-Z]{2}$'),
  document_type text not null,
  value_original text not null,
  value_normalized text not null,
  normalization_version text not null,
  created_at timestamptz not null default timezone('utc', now()),
  created_by text not null,
  foreign key (organization_id, person_id) references public.persons(organization_id, person_id),
  unique (organization_id, country_code, document_type, value_normalized)
);

create table if not exists public.person_contacts (
  contact_id uuid primary key default gen_random_uuid(),
  organization_id text not null,
  person_id uuid not null,
  kind text not null check (kind in ('email','phone')),
  value_original text not null,
  value_normalized text not null,
  label text,
  is_primary boolean not null default false,
  verified_at timestamptz,
  created_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now()),
  created_by text not null,
  updated_by text not null,
  foreign key (organization_id, person_id) references public.persons(organization_id, person_id),
  unique (organization_id, person_id, kind, value_normalized)
);
create unique index if not exists person_contacts_one_primary
  on public.person_contacts (organization_id, person_id, kind) where is_primary;

create table if not exists public.person_organization_links (
  link_id uuid primary key default gen_random_uuid(),
  organization_id text not null,
  person_id uuid not null,
  status text not null default 'active' check (status in ('active','inactive')),
  created_at timestamptz not null default timezone('utc', now()),
  created_by text not null,
  foreign key (organization_id, person_id) references public.persons(organization_id, person_id),
  unique (organization_id, person_id)
);

create table if not exists public.person_audit (
  audit_id uuid primary key default gen_random_uuid(),
  organization_id text not null,
  person_id uuid,
  actor_user_id text not null,
  action text not null,
  occurred_at timestamptz not null default timezone('utc', now()),
  correlation_id text not null,
  outcome text not null,
  entity_version bigint,
  foreign key (organization_id, person_id) references public.persons(organization_id, person_id)
);

create index if not exists persons_org_status_id on public.persons(organization_id, status, person_id);
create index if not exists persons_identifier_person on public.person_identifiers(organization_id, person_id);
create index if not exists persons_contact_person on public.person_contacts(organization_id, person_id);

do $$ declare t text; begin
  foreach t in array array['persons','person_identifiers','person_contacts','person_organization_links','person_audit'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('alter table public.%I force row level security', t);
    execute format('drop policy if exists persons_tenant_isolation on public.%I', t);
    execute format('create policy persons_tenant_isolation on public.%I using (organization_id = current_setting(''app.organization_id'', true)) with check (organization_id = current_setting(''app.organization_id'', true))', t);
  end loop;
end $$;

-- No service-role bypass is implied here. The host must use a role for which
-- FORCE RLS applies and must clear transaction settings on pooled connections.
