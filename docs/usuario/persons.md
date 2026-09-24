# Uso de Persons

La fachada `PersonsApi` devuelve diccionarios JSON-safe y errores sanitizados.
El caller entrega un `RequestContext` creado por el host autenticado; nunca
acepta `actor_user_id` u organización desde el body. Los IDs de otra
organización se comportan como `NOT_FOUND` después de autorizar.

Las mutaciones de un agregado existente requieren `expected_version`. Un
conflicto se reintenta sólo después de volver a leer y decidir; no hay
exactly-once implícito. Los candidatos de duplicado son explicables y no
fusionan personas.
# Alcance vigente

La fachada incluye persona física, nombres y contactos, `PersonAddress`,
género configurable, nacimiento/idioma/estado civil/fallecimiento,
identificadores fiscales y `PersonTaxProfile`. Las consultas requieren un
`RequestContext` confiable y autorización Core por operación; nunca se acepta
`organization_id` desde el body. La dirección, fiscalidad e Identity persistido
son siempre tenant-aware.
