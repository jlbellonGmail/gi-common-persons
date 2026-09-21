# Decision: 09-integracion-core-v021

## Estado

Estado técnico: ready_for_pr después de completar QA y revisión del diff.
La aprobación de merge corresponde exclusivamente al HITL en GitHub.

## Decisiones demostrables

- Se usa el wheel v0.2.1 publicado, no una ruta local ni una versión flotante.
- Core conserva la autoridad sobre organizaciones, memberships, permisos,
  roles, identidad y auditoría de autorización.
- Persons conserva la autoridad sobre Person y su auditoría de dominio.
- El boundary de identidad sólo transporta organization_id, actor/user IDs,
  subject y person_id opaco.
- Link/unlink delegan idempotencia y conflictos a Core y registran auditoría
  local sin exponer datos sensibles.
