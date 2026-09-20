# Mini-spec — 01-fundacion-diseno

## Alcance

Validar la fundación documental de Persons: límites de dominio, aislamiento
por organización, contrato de integración con Core `0.1.0`, exclusiones de
transporte/infraestructura y descomposición de unidades.

## Invariantes verificables

1. Persons no importa módulos de verticales ni accede APIs privadas de Core.
2. Cada dato de Persons queda bajo una `organization_id` y no existe consulta
   cross-tenant en la primera etapa.
3. La autorización se delega a `CoreApi.authorize` y falla cerrada ante
   respuesta incompleta, versión no soportada o error público de Core.
4. La implementación futura queda detrás de puertos y no decide una
   infraestructura no aprobada.

## Fuentes y límites

Las fuentes son `AGENTS.md`, `CONSTITUTION.md`, `ROADMAP.md`, `STATUS.md`,
`docs/tecnica/arquitectura-persons.md`, `contratos-persons.md`,
`modelo-persons.md`, `plan-persons.md` y la inspección del repositorio local
de Core. No se infieren catálogo documental, retención, permisos existentes,
RLS de producción ni contrato de identidad más allá de la evidencia observada.

## Criterio de salida

Review independiente aprobada, contrato de evidencia LIGHT satisfecho y
unidad lista para continuar con `02-contrato-core` sólo después del cierre
normal de esta unidad.
