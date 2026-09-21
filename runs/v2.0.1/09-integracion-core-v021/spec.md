# Spec — Integración Core v0.2.1

## Objetivo verificable

Persons instala y consume `gi-platform-core==0.2.1` desde su wheel publicado,
mantiene el tenant como `organization_id`, delega autorización y operaciones
de identidad a la API pública, registra auditoría y mantiene el `Person`
fuera de Core salvo su `person_id` opaco.

## Contratos

- CoreApi `0.1.0`: `authorize` con contexto coincidente.
- Identity `0.2.0`: `validate_identity`, `link_identity`, `unlink_identity`;
  compatible con CoreApi 0.1.0.
- Errores se convierten a categorías públicas de Persons sin propagar PII ni
  detalles de otro tenant.

## Exclusiones

Persons no crea organizaciones, usuarios, memberships, permisos ni roles; el
host/Core los provisiona. No se modifica GI-PLATFORM-CORE ni se hace merge.
