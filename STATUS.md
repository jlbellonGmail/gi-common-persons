# Estado operativo de GI-COMMON-PERSONS

Fecha de inspección: 2026-09-20. Estado: bootstrap local y diseño propuesto.

## Hechos

- Core y Template resueltos en C:\Proyectos; D:\proyectos no está disponible en esta sesión.
- No se encontró Persons bajo C:\Proyectos antes del bootstrap ni entre los repositorios visibles de jlbellonGmail.
- Core v0.1.0 y Template v2.0.1 publicados; commits exactos en README y expediente.
- Se prepara snapshot del circuito v2.0.1 y diseño; no se implementa producto.
- No se modificó Core, Template ni verticales. No se usaron datos ni credenciales de Supabase.
- No hay remoto, PR, CI ni aprobación HITL de Persons. No hay unidad completada.

## Pendientes materiales

1. RESUELTO: el usuario confirmó personas/documentos por organización y sin compartir entre tenants (2026-09-20).
2. Resolver mapeo seguro entre sujeto autenticado y user_id de Core y política de enlace Identity.
3. Resolver revocaciones/estados activos con el proveedor Core antes de habilitar producción.
4. Definir jurisdicciones/tipos de identificador iniciales, retención y borrado; no inventar normativa.
5. Confirmar remoto destino/visibilidad de Persons para iniciar unidad desde develop mediante el script oficial.

## Próximo paso

Revisar los diseños y las dependencias. Formalizar la unidad 01 con remoto real,
ASSESS sobre su diff y revisión del estado vigente. Continuar sólo la unidad no
bloqueada; no anunciar READY_FOR_PR mientras falten decisiones y evidencia.

El script heredado de STATUS imprime v2.0.0 en su bloque automático: es un valor
del motor del Template, no una versión de Persons. La procedencia real es v2.0.1.
Las advertencias sobre remoto/CI ausentes son esperadas y no equivalen a CI verde.
