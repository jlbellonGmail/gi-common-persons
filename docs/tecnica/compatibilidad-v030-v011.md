# Matriz de compatibilidad

| Componente | Versión | Contrato | Artefacto |
|---|---:|---|---|
| Core | `0.3.0` | Auth `0.1.0`, Identity `0.2.0`, Tenant `0.3.0` | GitHub Release `v0.3.0`, SHA256 `41830d62...537b47` |
| Tenants | `0.1.1` | `TenantContext`, `TenantService`, `TenantsApi` | GitHub Release `v0.1.1`, SHA256 `0d43d24d...c0bda7` |
| Persons | `0.1.0` | `PersonsApi` `0.1.0` | wheel de la PR #5 |

Los tres wheels se instalaron en un entorno virtual limpio. PyPI no ofrece los
paquetes. El wheel publicado de Tenants tiene metadata `0.1.1` pero módulo
`__version__ == 0.1.0`; la corrección está en PR #11 y no se modifica el tag.

Persons sólo usa APIs públicas y mantiene `organization_id` como frontera de
tenant; no consulta stores privados ni duplica organizaciones jurídicas.
