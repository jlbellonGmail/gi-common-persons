# Integración Core 0.3.0 / Tenants 0.1.1

Persons fija `gi-platform-core==0.3.0` y `gi-common-tenants==0.1.1`. Consume
CoreApi público para autorización e Identity y usa TenantContext/TenantsApi
como contrato de contexto, sin acceder a stores o tablas privadas. La matriz,
los hashes de tags, la discrepancia de metadatos y el bloqueo de PyPI están en
[compatibilidad-v030-v011](compatibilidad-v030-v011.md).

El vínculo jurídico/organizacional se referencia por `organization_id`; no se
duplican organizaciones de Core/Tenants. Toda operación Persons verifica el
contexto y falla cerrado ante denegación, aislamiento inconsistente o contrato
no soportado.
