# Decisión — Milestone 02–07 Persons

## Confirmado

Se implementa como biblioteca Python >=3.12, independiente del transporte.
PostgreSQL/Supabase es un adaptador de persistencia, no una dependencia de
runtime ni un despliegue. `organization_id` es el único límite tenant-aware.

## Dependencias bloqueantes conservadas

- D1: Core no ofrece resolución pública suficiente para habilitar enlace a
  Identity; la capacidad queda explícitamente deshabilitada.
- D2: el contrato observado no garantiza una política de frescura de
  revocaciones; la biblioteca exige respuesta coherente por operación y no
  promete habilitación productiva de permisos sin el host confiable.
- Catálogo de tipos documentales, retención y borrado no se inventan; las
  reglas se registran por el consumidor antes de habilitar cada tipo.

## Compatibilidad

No se modifica `gi-platform-core` ni verticales. El consumidor sólo tipa o
recibe un objeto compatible con `CoreApi` y procesa respuestas JSON públicas.
