# Unidad 08 — resumen

La migración y el hardening usan exclusivamente `persons.*` y fueron aplicados al proyecto `gi-dev` (`gletzbwuvmwjkmoufmyj`). La CLI continúa fallando contra `api.supabase.com`; el despliegue se verificó con el login role temporal de la API, en memoria, mediante el pooler PostgreSQL regional. No se registraron credenciales.

Verificación remota: esquema presente; cinco tablas; cuatro FK compuestas tenant-aware; trece índices; trece grants; quince políticas; cinco tablas con RLS habilitado y forzado; cuatro triggers; cero tablas Persons en `public`; cero políticas sin referencia tenant. La prueba Python real pasó (1 passed), cubriendo aislamiento entre dos organizaciones, unicidad, autorización, auditoría append-only y rollback.

La suite local tuvo 265 tests pasados y dos fallos de infraestructura en tests históricos de Git sobre directorios temporales (`Permission denied` al escribir `.git/objects`), no fallos de Persons. La unidad queda preparada para el gate `READY_FOR_PR`.
