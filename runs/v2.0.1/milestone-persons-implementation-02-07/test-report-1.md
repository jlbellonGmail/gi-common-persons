```yaml
status: approved
attempt: 1
feedback: []
```

# QA — Milestone 02–07 Persons

- `pytest tests_persons -q`: 16 passed.
- `pytest tests -q`: 267 passed in 380.03s.
- `python -m compileall -q gi_persons`: passed.
- Wheel reproducible de `gi-common-persons 0.1.0`: construido, hash registrado.
- `validate-supply-chain.ps1`: passed.
- `sync-agentic-adapters.ps1 -Check`: passed.
- Pruebas cubren aislamiento, autorización fail-closed, unicidad,
  normalización, candidatos, contactos, concurrencia, auditoría, cursor,
  errores sanitizados y migración/RLS estática.
