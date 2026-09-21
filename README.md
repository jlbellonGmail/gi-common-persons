# GI-COMMON-PERSONS

Biblioteca común tenant-aware para personas físicas del Sistema Integral GI.

La implementación vive en `gi_persons/` y es independiente del transporte y
de Dental, Law, CRM u otras verticales. Expone una fachada JSON-safe,
normalización determinista, concurrencia optimista, auditoría y puertos de
persistencia. `MemoryStore` sirve para pruebas; la migración PostgreSQL/RLS
está en `supabase/migrations/` y no se despliega automáticamente.

La integración de plataforma usa la superficie pública de
`gi-platform-core==0.2.1`: `CoreApi.authorize` (contrato 0.1.0) y
`validate_identity`, `link_identity`, `unlink_identity` (identidad 0.2.0).
Core recibe `person_id` como referencia opaca; nunca recibe el objeto Person.

Documentación: [implementación técnica](docs/tecnica/persons.md), [contratos](docs/tecnica/contrato-core.md), [modelo](docs/tecnica/modelo-persons.md) y [uso](docs/usuario/persons.md).

El circuito operativo procede del Template GI v2.0.1. La unidad vigente es el
Milestone `02-07-persons-implementation`; su evidencia está en
`runs/v2.0.1/milestone-02-07-persons-implementation/`.
