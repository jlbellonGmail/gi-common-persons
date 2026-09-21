# Integración Core v0.2.1

Estado: ready_for_pr
Versión: v2.0.1
Tipo: Feature
SDD: FULL
PR: pendiente
Merge: pendiente

## Objetivo

Instalar y consumir GI-PLATFORM-CORE v0.2.1 desde su wheel publicado con
identidad, autorización, aislamiento y auditoría tenant-aware.

## Resultado

La integración está implementada y validada: CoreApi 0.1.0 para autorización,
Identity 0.2.0 para resolución/link/unlink, y `person_id` opaco en el boundary.

## Cambios principales

- Dependencia fijada, fachada y puerto públicos ampliados.
- Link/unlink idempotente, conflictos y errores fail-closed.
- Pruebas consumidor, documentación y evidencia de instalación limpia.

## Validación

`267 passed`; la integración limpia instala Core 0.2.1 y verifica su hash.

## Decisiones

Core conserva organizaciones, usuarios, memberships, roles, permisos e
identidad. Persons conserva Person y su auditoría de dominio.

## Incidencias

La integración Supabase real se omite sin `PERSONS_TEST_DATABASE_URL`; no es
un fallo de esta unidad.

## Detalle

Ver `spec.md`, `validation-evidence.json`, `test-report-1.md`, `audit-1.md` y
`code-review-1.md`.
