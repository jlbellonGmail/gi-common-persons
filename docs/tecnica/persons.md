# Persons implementado

Persons es una biblioteca Python agnóstica del transporte. Su API recibe un
`RequestContext` confiable del host; no crea sesiones, usuarios, memberships ni
roles. El tenant es `organization_id` y todas las operaciones autorizan antes
de consultar.

## Core

El adaptador acepta exclusivamente la forma pública de `CoreApi.authorize` de
Core `0.1.0`. Debe devolver `contract_version: "0.1.0"`, `allowed: true` y un
contexto que coincida exactamente con usuario y organización solicitados. Un
error, versión desconocida, respuesta incompleta o contexto incoherente falla
cerrado. No se importan stores, tablas, entidades o adaptadores privados.

## Persistencia

`MemoryStore` es una referencia de pruebas. La migración
`supabase/migrations/20260920000100_persons.sql` define claves compuestas,
unicidad documental, principal único por tipo y RLS forzado. El host debe
establecer `SET LOCAL app.organization_id` dentro de una transacción y usar un
rol sin bypass de RLS; esta biblioteca no despliega ni conecta Supabase.

## Límites de identidad

No se habilita el enlace a Identity de Core: el contrato público observado no
resuelve todavía titularidad/correspondencia suficiente. No se infiere un
catálogo documental; el consumidor registra reglas país/tipo con versión.
Email y teléfono conservan el original y se normalizan sin transformar aliases
ni inferir país.

## Uso mínimo

```python
from gi_persons import IdentifierRule, IdentifierRules, MemoryStore, PersonsApi

rules = IdentifierRules()
rules.register(IdentifierRule("AR", "example", "1", lambda value: value.strip().upper()))
service = PersonsService(MemoryStore(), core_api, rules)
api = PersonsApi(service, cursor_secret=b"server-side secret")
```

El ejemplo requiere que el host suministre un `core_api` público y contexto
confiable; no incluye credenciales ni infraestructura.
