Estado: READY_FOR_PR
Versión: 0.1.0
Tipo: Milestone
SDD: FULL
PR: #5
Merge: no realizado

## Objetivo

Integrar Persons con Core 0.3.0 y Tenants 0.1.1 usando artefactos
reproducibles y APIs públicas.

## Resultado

La integración y el modelo físico/fiscal están implementados. La instalación
limpia desde wheels de GitHub Releases pasa; el wheel publicado de Tenants
conserva una discrepancia de módulo que se corrige en PR #11.

## Cambios principales

Direcciones, género configurable, datos opcionales, identificadores y perfiles
fiscales, Identity durable, auditoría, autorización, RLS y documentación.

## Validación

24 tests Persons y 4 de integración Core pasan; Supabase real queda omitido por
falta de `PERSONS_TEST_DATABASE_URL`. CI de PR #5 está verde.

## Decisiones

No se modifican tags/releases existentes ni se duplican datos privados de Core
o Tenants.

## Incidencias

PyPI no publica los paquetes. Tenants PR #11 corrige `__version__` en fuente;
el release asset existente no se sobrescribe.

## Detalle

Evidencia en `validation-evidence.md`, `test-report-1.md`, `audit-1.md` y
`code-review-1.md`. No hubo merge ni despliegue.
