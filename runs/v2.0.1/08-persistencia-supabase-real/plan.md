# Plan

1. Corregir la migración y declarar la configuración vinculada al proyecto confirmado.
2. Ejecutar `npx supabase db push` (CLI cacheada equivalente sólo como diagnóstico) y conservar salida.
3. Ejecutar pruebas PostgreSQL reales sobre esquema, índices, políticas, aislamiento, rollback y autorización.
4. Ejecutar suite local, contrato FULL, revisión independiente y sólo entonces preparar PR contra `develop`.

El paso 2 está bloqueado por transporte de la CLI antes de abrir conexión a la base.
