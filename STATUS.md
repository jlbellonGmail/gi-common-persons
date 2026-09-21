# Estado operativo de GI-COMMON-PERSONS

Fecha de inspección: 2026-09-21. Estado: Feature 09 en READY_FOR_PR; PR abierta y pendiente de decisión HITL.

## Hechos

- Core instalado y validado en versión `0.2.1`; Identity contract `0.2.0`.
- Persons consume Core únicamente mediante su API pública: CoreApi `0.1.0` e
  identidad `0.2.0`; Core recibe `person_id` como referencia opaca.
- La unidad vigente es Feature 09 `09-integracion-core-v021`, en READY_FOR_PR
  (`ROADMAP.md` conserva el estado `[-]`).
- Rama actual: `feature/v2.0.1-09-core-integration`; worktree actual:
  `C:\Proyectos\worktrees\v0.2.1-09-core-integration`.
- PR #4 está abierta contra `develop`:
  https://github.com/jlbellonGmail/gi-common-persons/pull/4
- CI vigente de la PR está verde: `circuit-tests`, `product-tests` y
  `local-reconciler-tests` completaron con éxito.
- El merge no se realizó. El gate `complete-approved-pr` permanece sin
  autorización HITL, como exige el circuito.
- Suite real: `267 passed in 422.90s`; Persons: `20 passed, 1 skipped` por
  ausencia de `PERSONS_TEST_DATABASE_URL` para Supabase local.
- Evidencia principal: `runs/v2.0.1/09-integracion-core-v021/`, incluyendo
  `test-report-1.md`, `audit-1.md`, `code-review-1.md` y
  `validation-evidence.json`.
- No se modificó GI-PLATFORM-CORE ni `develop`; no se usaron credenciales
  productivas de Supabase.

## Pendientes materiales

1. RESUELTO: el usuario confirmó personas/documentos por organización y sin compartir entre tenants (2026-09-20).
2. Esperar revisión humana y decisión `MERGE` o `NO MERGE` sobre la PR #4.
3. Si se aprueba, el circuito post-HITL debe verificar nuevamente CI antes de mergear.
4. Las decisiones de retención/borrado y cualquier despliegue real permanecen fuera de esta unidad.

## Próximo paso

Esperar revisión humana sobre la PR #4. No hacer merge automático ni cerrar la
unidad antes de una confirmación real de merge en `develop`.

El bloque automático puede conservar la versión del motor del Template; la
versión operativa de esta unidad es v2.0.1 y la dependencia integrada es Core
v0.2.1. La evidencia vigente de GitHub prevalece sobre cualquier snapshot.

## Verificación de esta reentrada (2026-09-21)

- Baseline inicial comprometida en `e9bdea8`.
- Template adoptado: `v2.0.1` / `fa8aade44fe808635e01916da7347b1d1837da7a`.
- Core público verificado en release `v0.2.1`; contratos `CoreApi 0.1.0` e
  Identity `0.2.0`.
- Suite completa: `267 passed in 422.90s`; suite Persons: `20 passed, 1 skipped`.
- PR #4 abierta contra `develop`, con CI verde y sin merge.
- Feature 09 publicada en la rama y worktree actuales, con ROADMAP en READY_FOR_PR.

<!-- STATUS:AUTO:BEGIN -->

## Estado verificado automáticamente

- Actualizado: 2026-09-21T13:32:30Z
- Versión: v2.0.0
- Rama: feature/v2.0.1-09-core-integration
- HEAD: 4d679e871d2e1f4692395d2797468ec8b06a90ff
- Remoto: https://github.com/jlbellonGmail/gi-common-persons.git
- Working tree: dirty
- Worktrees: 3
- Worktrees Git: 3
- Unidades activas: = [feature/v2.0.1-09-core-integration]; = [feature/v2.0.1-08-persistencia-supabase-real]
- PR activa: UNKNOWN / sin PR abierta
- CI: UNKNOWN / sin CI verificable
- CI vigente: UNKNOWN / sin CI verificable
- Última release: UNKNOWN / no disponible

<!-- STATUS:AUTO:END -->
