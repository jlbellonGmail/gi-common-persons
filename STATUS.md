# Estado operativo de GI-COMMON-PERSONS

## Unidad vigente (2026-09-24)

- Milestone `10-persons-v030-v011` en rama `milestone/10-persons-v030-v011`.
- Persons consume Core `0.3.0` y Tenants `0.1.1` por dependencias exactas.
- Implementación, migración, documentación y evidencia están terminadas para
  `READY_FOR_PR`; no se hizo merge.
- PyPI no ofrece ninguno de los paquetes: instalación pública bloqueada.
- Tags locales exactos, instalación limpia desde tags y compatibilidad pública
  verificados; Tenants conserva la discrepancia de `__version__ == 0.1.0`.
- QA Persons: `24 passed, 1 skipped` por falta de `PERSONS_TEST_DATABASE_URL`;
  la migración real no se ejecutó ni se desplegó.

Fecha de inspección: 2026-09-21. Estado: Feature 09 cerrada después del merge confirmado en `develop`.

## Hechos

- Core instalado y validado en versión `0.2.1`; Identity contract `0.2.0`.
- Persons consume Core únicamente mediante su API pública: CoreApi `0.1.0` e
  identidad `0.2.0`; Core recibe `person_id` como referencia opaca.
- Feature 09 `09-integracion-core-v021` está cerrada en `ROADMAP.md` (`[x]`).
- Checkout actual: rama `develop`, worktree `C:\Proyectos\gi-common-persons`.
- Worktree de la feature conservado, sin limpieza local automática:
  rama `feature/v2.0.1-09-core-integration`, ruta
  `C:\Proyectos\worktrees\v0.2.1-09-core-integration`.
- PR #4 fue mergeada contra `develop`:
  https://github.com/jlbellonGmail/gi-common-persons/pull/4
- Commit de merge confirmado: `97a75a9a53c970fe476a67978dd6165c7a7d035a`.
- CI de la PR fue verde: `circuit-tests`, `product-tests` y
  `local-reconciler-tests` completaron con éxito.
- El cierre remoto de ROADMAP fue validado por `close-feature.ps1` con el slug
  canónico y publicado en `origin/develop` mediante el commit `da3a341`.
- El primer workflow post-merge falló por recibir el slug incorrecto
  `09-core-integration`; se corrigió ejecutando el cierre canónico sin alterar
  Core ni realizar otro merge.
- Suite real: `267 passed in 422.90s`; Persons: `20 passed, 1 skipped` por
  ausencia de `PERSONS_TEST_DATABASE_URL` para Supabase local.
- Evidencia principal: `runs/v2.0.1/09-integracion-core-v021/`, incluyendo
  `test-report-1.md`, `audit-1.md`, `code-review-1.md` y
  `validation-evidence.json`.
- No se modificó GI-PLATFORM-CORE ni `develop`; no se usaron credenciales
  productivas de Supabase.

## Pendientes materiales

1. RESUELTO: el usuario confirmó personas/documentos por organización y sin compartir entre tenants (2026-09-20).
2. Mantener el worktree de la feature hasta una limpieza local explícita y segura.
3. Las decisiones de retención/borrado y cualquier despliegue real permanecen fuera de esta unidad.

## Próximo paso

Feature 09 está cerrada en remoto. No crear otra unidad ni modificar Core desde
este estado sin un nuevo alcance y evidencia.

El bloque automático puede conservar la versión del motor del Template; la
versión operativa de esta unidad es v2.0.1 y la dependencia integrada es Core
v0.2.1. La evidencia vigente de GitHub prevalece sobre cualquier snapshot.

## Verificación de esta reentrada (2026-09-21)

- Baseline inicial comprometida en `e9bdea8`.
- Template adoptado: `v2.0.1` / `fa8aade44fe808635e01916da7347b1d1837da7a`.
- Core público verificado en release `v0.2.1`; contratos `CoreApi 0.1.0` e
  Identity `0.2.0`.
- Suite completa: `267 passed in 422.90s`; suite Persons: `20 passed, 1 skipped`.
- PR #4 mergeada contra `develop` con CI verde; no se hizo ningún merge adicional.
- Feature 09 cerrada en `origin/develop` con ROADMAP en `[x]`.

<!-- STATUS:AUTO:BEGIN -->

## Estado verificado automáticamente

- Actualizado: 2026-09-21T14:34:27Z
- Versión: v2.0.0
- Rama: develop
- HEAD: 60a2c0a47bf5da8445974b724f9976565198c4ec
- Remoto: https://github.com/jlbellonGmail/gi-common-persons.git
- Working tree: dirty
- Worktrees: 3
- Worktrees Git: 3
- Unidades activas: ninguna
- PR activa: UNKNOWN / sin PR abierta
- CI: UNKNOWN / sin CI verificable
- CI vigente: UNKNOWN / sin CI verificable
- Última release: UNKNOWN / no disponible

<!-- STATUS:AUTO:END -->
