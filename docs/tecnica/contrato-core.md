# Contrato Core

El histórico de esta página describe Core 0.2.1. La compatibilidad vigente es
`gi-platform-core==0.3.0` y `gi-common-tenants==0.1.1`; ver la [matriz vigente](compatibilidad-v030-v011.md).
Persons consume sólo la API pública de Core: `CoreApi`
0.1.0 para autorización y el contrato de identidad 0.2.0 para resolución,
link y unlink. Se valida la versión, la organización y la coherencia del
contexto; la autorización falla cerrada. Core sólo recibe `person_id` como
referencia opaca. Stores, tablas, servicios y entidades privadas no forman
parte del contrato ni de los imports de Persons.
