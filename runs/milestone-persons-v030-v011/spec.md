# Intención y especificación

## Objetivo

Actualizar Persons para consumir exclusivamente las superficies públicas de
`gi-platform-core==0.3.0` y `gi-common-tenants==0.1.1`, manteniendo
`organization_id` como límite de tenant y completando el agregado de persona
física, fiscalidad, dirección, Identity durable y migración Supabase.

## Alcance verificable

- Dependencias exactas y matriz de compatibilidad documentadas.
- CoreApi `0.1.0`, Identity `0.2.0` y Tenant `0.3.0` verificados desde el tag
  Core `v0.3.0`; Tenants `v0.1.1` verificado por pyproject y API pública.
- API/modelos/memoria/DB para dirección, género, datos opcionales, fiscalidad
  e Identity persistido, siempre filtrados por organización.
- Migración en schema `persons` con PK/FK/índices, grants y RLS fail-closed.
- Pruebas unitarias, contrato de migración, integración Core y evidencia de
  instalación limpia; la prueba Supabase real sólo se marca ejecutada si hay
  credenciales.

## Fuera de alcance

No se modifican Core, Tenants, Template ni verticales; no se duplican datos de
organizaciones jurídicas; no se publican paquetes, tags, releases ni se hace
merge.

## Decisiones y supuestos

- `organization_id` es el tenant y aparece en todas las tablas de dominio.
- La autorización se delega al CoreApi por operación y toda denegación,
  contrato desconocido o proveedor caído falla cerrado.
- El catálogo fiscal es global por país/vigencia; perfiles, identificadores y
  datos de persona son tenant-aware.
- La discrepancia `gi-common-tenants` tag `v0.1.1`/`__version__ == 0.1.0`
  queda registrada como riesgo de upstream, sin corregir el repositorio ajeno.
