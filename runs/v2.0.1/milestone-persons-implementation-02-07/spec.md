# Spec — Milestone 02–07 Persons

## Alcance verificable

Implementar una biblioteca Python 3.12, sin transporte ni verticales, que
exponga operaciones JSON-safe para personas físicas tenant-aware. La única
dependencia de plataforma permitida es la superficie pública verificable de
`gi-platform-core` `0.1.0`: `CoreApi.authorize`, su respuesta JSON y errores
públicos. La persistencia productiva se entrega como puerto y migración
PostgreSQL/Supabase con RLS; no se conecta a un entorno real.

## Invariantes

- Todas las lecturas y escrituras reciben un contexto confiable y filtran por
  `organization_id`; una organización no puede observar otra.
- Una persona puede existir sin identificadores, y la unicidad documental es
  `(organization_id, country_code, document_type, normalized_value)`.
- La normalización de documentos requiere una regla explícita por país/tipo,
  conserva el original protegido y registra la versión de regla.
- Email y teléfono conservan el original, no son únicos globalmente y sólo
  tienen un principal por persona, tipo y organización.
- Las mutaciones existentes requieren `expected_version`; conflictos son
  deterministas y no pisan cambios.
- Duplicados exactos se rechazan; candidatos se explican por coincidencias
  deterministas y nunca fusionan automáticamente.
- Auditoría append-only no contiene PII ni payloads de solicitud.
- Autorización desconocida, inconsistente, no permitida o Core indisponible
  falla cerrado con un error Persons sanitizado.
- `link_identity` permanece deshabilitado hasta existir el contrato público de
  resolución/titularidad de Core identificado como D1 en la arquitectura.

## Fuera de alcance

No se agregan endpoints HTTP, credenciales, usuarios, membership, roles,
tablas de Core, consultas privadas, sincronización con verticales, fusión,
catálogo documental inventado, retención legal ni despliegue Supabase.
