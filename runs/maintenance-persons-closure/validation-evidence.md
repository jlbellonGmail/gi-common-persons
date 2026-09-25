# Evidencia de cierre de Persons

Fecha: 2026-09-25

## Merge y reconciliación

- PR #5 está `MERGED` en `develop` con merge commit
  `4e0bf72932cb42c71ff701ee21e6167f3d6433a1`.
- `ROADMAP.md` marca Unidad 10 como `[x]`.
- El reconciliador oficial eliminó el worktree y la rama de la Unidad 10.
- `develop` local está sincronizado con `origin/develop` en `ae02e4c`.

## Reconciliador

- El CI inicial `36075235724` falló en `test_start_reconciler_from_linked_worktree`
  porque no observó lock/log en 60 segundos; los otros seis tests pasaron.
- El test puntual pasó cinco veces en Windows local.
- El rerun del mismo workflow `36075235724` pasó: `circuit-tests`,
  `product-tests` y `local-reconciler-tests` verdes.
- No se aumentaron timeouts ni se ocultaron fallos; el resultado se trató como
  una flake de arranque del runner porque no se reprodujo localmente y el rerun
  pasó sin cambios de código.

## Supabase

- `PERSONS_TEST_DATABASE_URL` no está definido en el entorno actual; la prueba
  PostgreSQL/Supabase real queda bloqueada y no se declara ejecutada.

## Dependencias, contratos y modelo

- Entorno virtual limpio instalado desde los wheels de GitHub Releases:
  Core distribución `0.3.0`, Tenants distribución `0.1.1`, Persons `0.1.0`.
- Contratos públicos importados: `CoreApi`, `CoreApi.authorize`,
  `validate_identity`, `link_identity`, `unlink_identity`, `Tenant`,
  `TenantContext` e `IDENTITY_CONTRACT_VERSION == 0.2.0`; `TenantContext` de
  Tenants también fue importado.
- Persons en entorno limpio: `24 passed, 1 skipped`; el skip corresponde a
  la ausencia de `PERSONS_TEST_DATABASE_URL`.
- La inspección estática de las migraciones encontró 11 tablas Persons,
  7 grants, 11 índices, 2 tablas con FORCE RLS, 7 políticas y políticas
  condicionadas por `app.organization_id`.
- El modelo/API vigente contiene personas, identificadores generales y
  fiscales, direcciones, contactos, género configurable, campos opcionales,
  categorías/perfiles fiscales, vínculos organizacionales, Identity durable,
  auditoría, autorización fail-closed y claves `organization_id`.

## Gates y revisión

- `circuit-tests`, `product-tests` y `local-reconciler-tests` del rerun
  `36075235724`: verdes.
- `check-integrity.ps1`: PASS para ROADMAP/runs/SUMMARY/Git/STATUS.
- La auditoría y code review independientes de la Unidad 10 permanecen en
  `runs/milestone-persons-v030-v011/audit-1.md` y
  `runs/milestone-persons-v030-v011/code-review-1.md`, ambas aprobadas antes
  del merge.
