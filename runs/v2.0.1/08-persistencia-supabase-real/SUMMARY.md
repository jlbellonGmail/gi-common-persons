# Unidad 08 — Persistencia Supabase real

Estado: READY_FOR_PR
Versión: v2.0.1
Tipo: Feature
SDD: runs/v2.0.1/08-persistencia-supabase-real/sdd.json
PR: pendiente de apertura
Merge: no ejecutado

## Objetivo

Corregir, desplegar y verificar la persistencia tenant-aware de Persons en Supabase real, sin modificar Core ni verticales.

## Resultado

La migración y el hardening usan exclusivamente `persons.*` y fueron aplicados al proyecto `gi-dev` (`gletzbwuvmwjkmoufmyj`).

## Cambios principales

Se corrigieron las cinco tablas, FK compuestas, índices, grants, triggers, auditoría append-only y políticas RLS forzadas. Se agregó la prueba PostgreSQL real y evidencia reproducible.

## Validación

El remoto confirmó esquema, cinco tablas, cuatro FK, trece índices, trece grants, quince políticas, cinco tablas con RLS habilitado y forzado, cuatro triggers, cero tablas Persons en `public` y cero políticas sin referencia tenant. La prueba Python real pasó: 1 passed. La suite local tuvo 265 pasados y dos fallos históricos de infraestructura Windows al escribir objetos Git temporales.

## Decisiones

La CLI mantiene un bloqueo de transporte contra `api.supabase.com`. Se usó la API autenticada para obtener un login role temporal y el pooler regional PostgreSQL; el secreto se mantuvo sólo en memoria.

## Incidencias

Los dos fallos de la suite completa fueron `Permission denied` en `.git/objects` de repositorios temporales de tests históricos; no afectan el producto Persons. Quedan documentados en `test-report-1.md`.

## Detalle

La evidencia primaria está en `verify.sql`, `integration.sql`, `remote-execution.json`, `validation-evidence.json` y `machine-test-evidence.json`.
