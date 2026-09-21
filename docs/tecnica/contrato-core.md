# Contrato Core

Persons consume sólo la API pública de `gi-platform-core==0.2.1`: `CoreApi`
0.1.0 para autorización y el contrato de identidad 0.2.0 para resolución,
link y unlink. Se valida la versión, la organización y la coherencia del
contexto; la autorización falla cerrada. Core sólo recibe `person_id` como
referencia opaca. Stores, tablas, servicios y entidades privadas no forman
parte del contrato ni de los imports de Persons.
