# 02-07-persons-implementation — implementación común de Persons

Estado: EN_REVISIÓN
Versión: v2.0.1
Tipo: Milestone
SDD: FULL
PR: pendiente
Merge: no realizado

## Objetivo

Implementar en una única unidad funcional las Unidades 02–07: contrato
CoreApi, dominio Person, identificadores, deduplicación, contactos, vínculos,
persistencia/RLS, fachada pública, pruebas, CI, auditoría y documentación.

## Resultado

La biblioteca `gi_persons` y la migración Supabase/RLS fueron implementadas sin
dependencias hacia Core privado o verticales. La validación local específica de
Persons pasó 16 tests y la suite del Template pasó 267 tests.

## Cambios principales

- Modelos tenant-aware, normalización explícita por país/tipo/version, unicidad
  documental y candidatos deterministas.
- CoreApi fail-closed, errores sanitizados, optimistic locking y auditoría
  append-only atómica en el adaptador de referencia.
- Contactos email/teléfono no destructivos, principal único y enlace Identity
  deshabilitado por dependencia D1.
- Puerto DB-API, migración PostgreSQL/Supabase con FKs compuestas, índices y
  `FORCE ROW LEVEL SECURITY`.
- Fachada JSON-safe con cursor firmado, tests de consumidor y documentación.

## Validación

- `pytest tests_persons -q`: 16 passed.
- `pytest tests -q`: 267 passed in 380.03s.
- `python -m compileall -q gi_persons`: passed.
- `python -m pip wheel . --no-deps --no-build-isolation`: passed; hash en
  `validation-evidence.json`.
- `validate-supply-chain.ps1`: passed.
- `sync-agentic-adapters.ps1 -Check`: passed.
- Evidencia de máquina: `machine-test-evidence.json`.

## Decisiones

- No se inventan tipos documentales: el consumidor debe registrar cada regla.
- No se habilita Identity link por falta de contrato público suficiente en Core.
- Supabase es un adaptador/migración; no se conecta ni despliega un entorno
  real, y RLS efectivo exige un rol sin bypass y settings transaccionales.
- La PR final se dejará `READY_FOR_PR` y habrá un único HITL de MERGE/NO MERGE.

## Incidencias

- D1 y D2 permanecen documentadas como bloqueos de capacidades concretas, no
  de la biblioteca base: resolución/titularidad de Identity y frescura de
  revocaciones de autorización.
- La suite del Template tuvo un primer run combinado con fallos transitorios
  de subprocess en Windows; el rerun canónico `pytest tests -q` pasó completo.

## Detalle

El milestone no despliega infraestructura, no modifica Core ni verticales y
no declara una release. La revisión final debe inspeccionar el diff vigente,
la migración y la evidencia FULL antes de `ready-for-pr.ps1`.
