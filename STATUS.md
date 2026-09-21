# Estado operativo de GI-COMMON-PERSONS

Fecha de inspección: 2026-09-21. Estado: Feature 09 en implementación avanzada; pendiente de gates finales, PR y HITL.

## Hechos

- Core y Template resueltos en C:\Proyectos; D:\proyectos no está disponible en esta sesión.
- No se encontró Persons bajo C:\Proyectos antes del bootstrap ni entre los repositorios visibles de jlbellonGmail.
- Core v0.2.1 publicado como wheel; contratos públicos CoreApi 0.1.0 e Identity 0.2.0 verificados.
- Persons consume Core sólo por CoreApi público; link/unlink y resolución son tenant-aware y usan person_id opaco.
- La rama de trabajo es `feature/v2.0.1-09-core-integration`; no se modificó `develop` ni Core.
- No se modificó Core, Template ni verticales. No se usaron datos ni credenciales de Supabase.
- No hay remoto, PR, CI ni aprobación HITL de Persons. No hay unidad completada.

## Pendientes materiales

1. RESUELTO: el usuario confirmó personas/documentos por organización y sin compartir entre tenants (2026-09-20).
2. Ejecutar suite completa estable y gates de contrato/revisión sobre el diff vigente.
3. Publicar PR contra `develop` y esperar CI; el merge queda reservado al HITL.
4. Definir jurisdicciones/tipos de identificador iniciales, retención y borrado; no inventar normativa.
5. Las decisiones de retención/borrado y cualquier despliegue real permanecen fuera de esta unidad.

## Próximo paso

Completar QA/gates, ejecutar `ready-for-pr.ps1`, publicar la rama y crear la PR.
No hacer merge automático ni desplegar infraestructura desde esta rama.

El script heredado de STATUS imprime v2.0.0 en su bloque automático: es un valor
del motor del Template, no una versión de Persons. La procedencia real es v2.0.1.
Las advertencias sobre remoto/CI ausentes son esperadas y no equivalen a CI verde.

## Verificación de esta reentrada (2026-09-20)

- Baseline inicial comprometida en `e9bdea8`.
- Template adoptado: `v2.0.1` / `fa8aade44fe808635e01916da7347b1d1837da7a`.
- Core público inspeccionado en `v0.1.0` / `673a9a8`; Persons sólo puede
  consumir `CoreApi`, respuestas JSON y errores públicos.
- Suite del circuito: `267 passed in 426.97s`.
- No existe `origin`, PR, CI ni work unit oficial iniciada.
- No se implementó producto ni se modificaron Core o verticales.

<!-- STATUS:AUTO:BEGIN -->

## Estado verificado automáticamente

- Actualizado: 2026-09-21T13:13:02Z
- Versión: v2.0.0
- Rama: feature/v2.0.1-09-core-integration
- HEAD: e98a28844610793c03807437346703a563deb41f
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
