select json_build_object(
  'schema', (select count(*) = 1 from pg_namespace where nspname = 'persons'),
  'tables', (select coalesce(json_agg(table_name order by table_name), '[]'::json)
             from information_schema.tables where table_schema = 'persons'),
  'rls', (select coalesce(json_agg(json_build_object('table', c.relname, 'enabled', c.relrowsecurity, 'forced', c.relforcerowsecurity) order by c.relname), '[]'::json)
          from pg_class c join pg_namespace n on n.oid = c.relnamespace
          where n.nspname = 'persons' and c.relkind = 'r'),
  'constraints', (select coalesce(json_agg(json_build_object('table', conrelid::regclass::text, 'name', conname, 'type', contype, 'definition', pg_get_constraintdef(oid)) order by conrelid::regclass::text, conname), '[]'::json)
                  from pg_constraint where connamespace = 'persons'::regnamespace),
  'indexes', (select coalesce(json_agg(json_build_object('table', tablename, 'name', indexname, 'definition', indexdef) order by tablename, indexname), '[]'::json)
             from pg_indexes where schemaname = 'persons'),
  'grants', (select coalesce(json_agg(json_build_object('table', table_name, 'privilege', privilege_type) order by table_name, privilege_type), '[]'::json)
            from information_schema.role_table_grants where table_schema = 'persons' and grantee = 'authenticated'),
  'policies', (select coalesce(json_agg(json_build_object('table', tablename, 'name', policyname, 'command', cmd, 'using', qual, 'check', with_check) order by tablename, policyname), '[]'::json)
              from pg_policies where schemaname = 'persons'),
  'triggers', (select coalesce(json_agg(json_build_object('table', event_object_table, 'name', trigger_name, 'event', event_manipulation) order by event_object_table, trigger_name), '[]'::json)
              from information_schema.triggers where trigger_schema = 'persons')
);
