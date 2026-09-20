# ROADMAP

Plan de fundación; sin versión de release decidida. Todas las unidades siguen
pendientes hasta atravesar el circuito real. El expediente bootstrap no las cierra.

- [x] 01-fundacion-diseno — consolidar decisiones, procedencia y contratos; completar adopción del circuito y revisión independiente.
- [x] 02-contrato-core — pruebas consumidor/proveedor de la superficie pública y resolución de dependencias de seguridad.
- [x] 03-personas-identificadores — agregado Person, normalización y unicidad transaccional por organización.
- [x] 04-contactos-vinculos — contactos, vínculo organizacional y enlace Identity opcional cuando exista contrato suficiente.
- [x] 05-persistencia-aislamiento — adaptador persistente, aislamiento efectivo, concurrencia y auditoría atómica.
- [x] 06-api-publica — fachada versionada, errores, paginación y pruebas de consumidores sin dependencias inversas.
- [x] 07-readiness-integracion — CI real, auditoría, contrato de distribución y evidencia para HITL.
- [ ] 08-persistencia-supabase-real — corregir, validar, desplegar y verificar la migración tenant-aware en Supabase real.

Referencias y aceptación: [plan técnico](docs/tecnica/plan-persons.md).
`[ ]` pendiente; `[-]` sólo READY_FOR_PR real; `[x]` sólo después del merge
confirmado a develop. No se decide un tag ni una release en este documento.




