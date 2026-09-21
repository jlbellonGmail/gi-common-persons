# Integración GI-PLATFORM-CORE v0.2.1

Persons declara `gi-platform-core==0.2.1`. La release publicada se instala
desde el asset de GitHub Release porque Core no se distribuye en PyPI:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install `
  https://github.com/jlbellonGmail/gi-platform-core/releases/download/v0.2.1/gi_platform_core-0.2.1-py3-none-any.whl
.\.venv\Scripts\python -m pip install --no-deps -e .
```

El wheel verificado para esta unidad tiene SHA-256
`9bc4c04ff0136a25559fb428aa8fd3a2e84ae69589a44fdd2ed9f91dd6a352cb`.

## Contratos consumidos

- `CoreApi` `contract_version=0.1.0`: `authorize` se ejecuta antes de cada
  lectura o mutación de Persons. Organizations, usuarios, memberships, roles,
  permisos y estados activos siguen siendo propiedad de Core.
- Identidad `contract_version=0.2.0`: `validate_identity`, `link_identity` y
  `unlink_identity` son operaciones públicas aditivas y compatibles con 0.1.0.

El host crea `RequestContext` sólo después de autenticar al actor. Persons
comprueba siempre `user_id`, `organization_id` y `location_id` del contexto;
no toma actor ni tenant del body. Al vincular, valida que el Person existe en
la organización y pasa a Core únicamente el `person_id` string, como
referencia opaca. No importa stores, tablas, servicios ni entidades internas
de Core.

## Flujo de identidad

1. El host obtiene el `user_id`, `external_subject` y organización del actor.
2. `resolve_identity` llama `CoreApi.validate_identity` y exige identidad
   activa, membership activa, subject exacto y organización coincidente.
3. `link_identity` autoriza `persons:identity:link`, vuelve a comprobar el
   Person en el tenant y llama a Core, que aplica `organization:identity_link`.
4. `unlink_identity` repite la autorización tenant-aware y llama a Core con
   `organization:identity_unlink`.
5. Core y Persons registran auditoría. Persons registra sólo actor, tenant,
   acción, referencia Person, correlación, resultado y versión; no PII.

Link y unlink son idempotentes según el contrato 0.2.0. Un conflicto, una
respuesta de contrato incorrecta, una identidad de otro tenant o un fallo del
proveedor se traduce a un error público seguro y no revela datos cruzados.

## Operación local

Para probar la integración completa, configure las organizaciones, usuarios,
memberships, permisos y roles en Core mediante `CoreApi`; Persons no los crea
automáticamente al crear un Person. Ejecute:

```powershell
python -m pytest tests_persons -q
python -m pytest -q
```

La prueba de integración usa únicamente `CoreApi` e `InMemoryCoreStore` de la
dependencia instalada. La prueba Supabase es optativa y requiere un entorno
local configurado; no usa credenciales productivas.
