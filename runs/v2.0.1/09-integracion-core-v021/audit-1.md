```yaml
status: approved
attempt: 1
feedback: []
```

# Auditoría — Integración Core v0.2.1

- Dependencia exacta y hash de wheel registrados; no se usa PyPI flotante ni
  ruta local en `pyproject.toml`.
- Producción de Persons no importa stores, tablas, servicios ni entidades
  internas de Core; el puerto sólo declara métodos de `CoreApi` público.
- Cada caso de uso autoriza con actor y organización; respuestas con versión,
  tenant o identidad incoherentes fallan cerradas.
- El boundary de link/unlink sólo pasa `person_id`, `organization_id`, actor,
  user_id y subject; no pasa el objeto Person ni PII del agregado.
- La auditoría local no registra nombres, documentos, email, teléfono ni
  credenciales. Core mantiene su propia auditoría de autorización/identidad.
- No hay cambios fuera de `gi-common-persons`, no hay merge ni despliegue.
