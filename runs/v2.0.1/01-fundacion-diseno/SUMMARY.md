# 01-fundacion-diseno — fundación documental y contrato

Estado: EN_REVISIÓN
Versión: v2.0.1
Tipo: Feature
SDD: LIGHT
PR: no creada
Merge: no realizado

## Objetivo

Consolidar la procedencia del Template, la dependencia pública verificable de
Core y los límites funcionales de Persons antes de implementar producto.

## Resultado

El baseline `40837d6` fue publicado en `origin/develop`. Se creó la work unit
oficial en el worktree generado por el Template. ASSESS determinista clasificó
el alcance documental como `LOW` / `LIGHT`.

## Cambios principales

- Se conservaron la arquitectura, el modelo, los contratos y el plan de
  Persons como diseño previo trazable.
- Se fijó Core `v0.1.0` en SHA `673a9a8` y Template `v2.0.1` en SHA
  `fa8aade44fe808635e01916da7347b1d1837da7a`.
- Se registró que Persons sólo consume `CoreApi`, respuestas JSON y errores
  públicos; no se acceden stores, tablas ni entidades privadas.

## Validación

- `pytest -q`: `267 passed in 426.97s` sobre el baseline.
- `check-integrity.ps1`: PASS.
- `check-status.ps1`: PASS, con advertencias esperadas por CI aún no creado.
- `assess-work-unit.ps1`: PASS, `LOW` / `LIGHT`.
- `materialize-sdd.ps1`: PASS, SDD adaptativo `LIGHT`.

## Decisiones

- El tenant es `organization_id`; no existe intercambio ni búsqueda global en
  la primera etapa.
- No se habilita `link_identity` hasta contar con contrato público verificable
  para resolución y validación del sujeto de Core.
- No se elige ni despliega infraestructura de persistencia en esta unidad.

## Incidencias

- El repositorio remoto fue creado vacío y ya contiene el baseline en
  `develop`; aún no hay PR ni CI de Persons.
- Las decisiones de catálogo documental, persistencia efectiva y estados de
  autorización siguen siendo entradas de las unidades posteriores.

## Detalle

La unidad no declara implementación funcional ni readiness para PR. Su review
debe validar procedencia, límites, ausencia de dependencias inversas y que los
bloqueos queden derivados a unidades posteriores.
