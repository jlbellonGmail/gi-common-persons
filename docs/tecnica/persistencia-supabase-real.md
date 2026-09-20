# Persistencia Supabase real de Persons

La Unidad 08 despliega exclusivamente el esquema `persons` en el proyecto Supabase `gi-dev` (`gletzbwuvmwjkmoufmyj`). Las cinco tablas son tenant-aware mediante `organization_id`, FK compuestas e índices por organización.

La migración habilita y fuerza RLS, concede sólo los privilegios necesarios a `authenticated`, impone unicidad de identificadores por organización y mantiene `person_audit` append-only. Las políticas comparan `organization_id` con `current_setting('app.organization_id', true)` y fallan cerrado si falta el contexto.

La verificación remota confirmó cinco tablas, cuatro FK, trece índices, trece grants, quince políticas, cinco tablas con RLS forzado, cuatro triggers y cero tablas Persons en `public`. La evidencia está en `runs/v2.0.1/08-persistencia-supabase-real/`.

La CLI presentó un error de transporte contra `api.supabase.com`; el despliegue se ejecutó mediante un login role temporal obtenido por la API autenticada y el pooler PostgreSQL regional. No se persistieron credenciales.
