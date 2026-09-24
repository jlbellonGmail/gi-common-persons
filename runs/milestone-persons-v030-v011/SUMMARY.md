Estado: READY_FOR_PR
Versión: 0.1.0
Tipo: Milestone
SDD: FULL
PR: pendiente de creación por el gate
Merge: no realizado

## Objetivo

Actualizar Persons para Core 0.3.0 y Tenants 0.1.1 y completar persona física,
fiscalidad, Identity durable, API y persistencia tenant-aware.

## Resultado

Implementación y evidencia listas para PR; `organization_id` sigue siendo el
tenant y la autorización es fail-closed mediante CoreApi.

## Cambios principales

Se agregaron dirección, género configurable, datos opcionales, identificadores
fiscales, perfil/catálogo fiscal, Identity persistido, migración Supabase,
compatibilidad pública y documentación.

## Validación

24 pruebas Persons pasaron y una prueba Supabase real fue omitida por falta de
credenciales. Core/Tenants se instalaron desde tags locales exactos en venv;
PyPI no ofrece los paquetes.

## Decisiones

No se duplican organizaciones jurídicas ni stores privados; Core y Tenants se
consumen por APIs públicas y el catálogo fiscal es global por país/vigencia.

## Incidencias

La disponibilidad pública de ambos paquetes está bloqueada. Tenants `v0.1.1`
declara `__version__ == 0.1.0`; se documentó sin modificar el upstream.

## Detalle

La evidencia completa está en `validation-evidence.md`, `test-report-1.md`,
`audit-1.md` y `code-review-1.md`. No hubo merge, release ni despliegue.
