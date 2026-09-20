# Contrato Core

Persons consume sólo `CoreApi.authorize` de Core `0.1.0`, su JSON público y
errores públicos. Se valida `contract_version`, autorización positiva y
coherencia exacta del contexto. Stores, tablas y entidades privadas no forman
parte del import ni del contrato.
