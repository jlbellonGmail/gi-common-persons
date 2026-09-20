# Api Publica

`PersonsApi` es una fachada sin transporte: entrega resúmenes JSON-safe,
errores categorizados y cursores firmados ligados a organización y filtros.
Los límites de consulta son acotados y las mutaciones exigen
`expected_version`.
