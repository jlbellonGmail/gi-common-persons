# Matriz de compatibilidad

| Componente | Versión consumida | Contrato público verificado | Evidencia |
|---|---:|---|---|
| GI Platform Core | `0.3.0` | `CoreApi` auth `0.1.0`, Identity `0.2.0`, Tenant `0.3.0` | tag local `6b10d564`, manifest `core-api-v0.3.0` |
| GI Common Tenants | `0.1.1` | `TenantContext`, `TenantService`, `TenantsApi` | tag local `8af783f8`, pyproject e init |
| Persons | `0.1.0` | `PersonsApi` `0.1.0` | `gi_persons/api.py` |

Los tags fueron verificados sin modificar esos repositorios. `pip index
versions` no encontró ninguno de los paquetes; la instalación limpia desde
índice queda bloqueada. La instalación editable local produjo metadatos
`0.3.0` y `0.1.1`; el módulo Tenants expone `__version__ == 0.1.0`,
discrepancia upstream registrada y no corregida aquí.

Persons no importa stores, tablas, CoreService ni entidades privadas. `Person`
mantiene referencias opacas a `core_user_id`; la organización jurídica y su
identidad técnica pertenecen a Core/Tenants.
