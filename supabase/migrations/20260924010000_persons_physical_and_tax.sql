-- Persons v0.1.1: physical-person, address, identity and tax extensions.
alter table persons.person add column if not exists gender_code text;
alter table persons.person add column if not exists language_code text;
alter table persons.person add column if not exists marital_status text;
alter table persons.person add column if not exists death_date date;
alter table persons.person add constraint person_dates_valid check (death_date is null or birth_date is null or death_date >= birth_date);

create table if not exists persons.person_address (
 organization_id text not null, address_id uuid not null default gen_random_uuid(), person_id uuid not null,
 address_type text not null check (address_type in ('home','work','billing','other')), line1 text not null,
 line2 text, city text, region text, postal_code text, country_code text not null check (country_code ~ '^[A-Z]{2}$'),
 is_primary boolean not null default false, created_at timestamptz not null default timezone('utc',now()), updated_at timestamptz not null default timezone('utc',now()),
 primary key (organization_id,address_id), foreign key (organization_id,person_id) references persons.person(organization_id,person_id) on delete restrict
);
create unique index if not exists person_address_primary on persons.person_address(organization_id,person_id,address_type) where is_primary;
create index if not exists person_address_by_person on persons.person_address(organization_id,person_id);

create table if not exists persons.gender_option (
 organization_id text not null, code text not null, label text not null, active boolean not null default true,
 primary key (organization_id,code)
);

create table if not exists persons.person_identity (
 organization_id text not null, identity_id uuid not null default gen_random_uuid(), person_id uuid not null,
 core_user_id text not null, external_subject text not null, status text not null default 'active' check (status in ('active','inactive')),
 created_at timestamptz not null default timezone('utc',now()), updated_at timestamptz not null default timezone('utc',now()),
 primary key (organization_id,identity_id), foreign key (organization_id,person_id) references persons.person(organization_id,person_id) on delete restrict,
 unique (organization_id,core_user_id)
);
create unique index if not exists person_identity_active_unique on persons.person_identity(organization_id,person_id) where status = 'active';

create table if not exists persons.tax_category (
 category_id uuid primary key default gen_random_uuid(), country_code text not null check (country_code ~ '^[A-Z]{2}$'),
 code text not null, label text not null, valid_from date not null, valid_to date, unique(country_code,code,valid_from), check(valid_to is null or valid_to >= valid_from)
);
create table if not exists persons.person_tax_identifier (
 organization_id text not null, tax_identifier_id uuid not null default gen_random_uuid(), person_id uuid not null,
 country_code text not null check (country_code ~ '^[A-Z]{2}$'), identifier_type text not null, value_original text not null, value_normalized text not null,
 created_at timestamptz not null default timezone('utc',now()), primary key(organization_id,tax_identifier_id), foreign key(organization_id,person_id) references persons.person(organization_id,person_id) on delete restrict,
 unique(organization_id,country_code,identifier_type,value_normalized)
);
create table if not exists persons.person_tax_profile (
 organization_id text not null, profile_id uuid not null default gen_random_uuid(), person_id uuid not null, country_code text not null,
 category_code text not null, valid_from date not null, valid_to date, version bigint not null default 1,
 primary key(organization_id,profile_id), foreign key(organization_id,person_id) references persons.person(organization_id,person_id) on delete restrict,
 foreign key(country_code,category_code,valid_from) references persons.tax_category(country_code,code,valid_from), unique(organization_id,person_id,country_code), check(valid_to is null or valid_to >= valid_from)
);
create index if not exists person_tax_identifier_by_person on persons.person_tax_identifier(organization_id,person_id);
create index if not exists person_tax_profile_by_person on persons.person_tax_profile(organization_id,person_id);

grant select,insert,update on persons.person_address, persons.gender_option, persons.person_identity, persons.person_tax_identifier, persons.person_tax_profile to authenticated;
grant select on persons.tax_category to authenticated;
do $$ declare t text; begin foreach t in array array['person_address','gender_option','person_identity','person_tax_identifier','person_tax_profile','tax_category'] loop
 execute format('alter table persons.%I enable row level security',t); execute format('alter table persons.%I force row level security',t);
 execute format('drop policy if exists persons_tenant_select on persons.%I',t); execute format('drop policy if exists persons_tenant_insert on persons.%I',t); execute format('drop policy if exists persons_tenant_update on persons.%I',t);
 if t = 'tax_category' then execute format('create policy persons_tenant_select on persons.%I for select using (true)',t); else
 execute format('create policy persons_tenant_select on persons.%I for select using (organization_id = current_setting(''app.organization_id'',true))',t);
 execute format('create policy persons_tenant_insert on persons.%I for insert with check (organization_id = current_setting(''app.organization_id'',true))',t);
 execute format('create policy persons_tenant_update on persons.%I for update using (organization_id = current_setting(''app.organization_id'',true)) with check (organization_id = current_setting(''app.organization_id'',true))',t); end if; end loop; end $$;
