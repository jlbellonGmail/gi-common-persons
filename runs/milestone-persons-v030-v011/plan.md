# Plan

1. Fijar dependencias y adaptar contratos públicos/versiones.
2. Extender dominio, puertos, memoria, servicio y fachada pública.
3. Crear migración incremental tenant-aware con RLS, grants e índices.
4. Añadir pruebas de aislamiento, autorización, idempotencia, conflicto,
   auditoría, Core/Tenants y contrato SQL.
5. Actualizar documentación/matriz, ejecutar gates, revisión independiente y
   dejar PR abierta contra `develop`.
