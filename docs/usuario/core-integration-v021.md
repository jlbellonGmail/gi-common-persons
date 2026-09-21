# Uso de Core v0.2.1 desde Persons

El host entrega un `CoreApi` público y un `RequestContext` confiable:

```python
from gi_persons import IdentifierRules, MemoryStore, PersonsService, RequestContext

service = PersonsService(MemoryStore(), core_api, IdentifierRules())
context = RequestContext(user_id=actor_id, organization_id=organization_id)
person = service.create_person(context, "Ada Lovelace")
service.resolve_identity(context, core_user_id, external_subject)
service.link_identity(context, person.person_id, core_user_id, external_subject)
service.unlink_identity(context, person.person_id)
```

Antes de usar el ejemplo, Core debe tener una organización activa, el usuario
y su membership activa, permisos y un rol asignado. La autorización deniega
por defecto. Un Person se busca siempre dentro de `organization_id`; un ID de
otro tenant no permite resolverlo ni modificarlo.

Para instalar en una máquina limpia, siga la [guía técnica de integración
Core v0.2.1](../tecnica/core-integration-v021.md). La dependencia se fija en
`gi-platform-core==0.2.1` y se verifica con el hash publicado de su wheel.
