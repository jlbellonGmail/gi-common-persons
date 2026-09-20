# Persistencia real de Persons

Persons guarda sus datos en el esquema PostgreSQL `persons`, separado de `public` y aislado por `organization_id`.

La aplicación debe establecer `app.organization_id` en cada transacción antes de usar las tablas. RLS impide leer o modificar datos de otra organización; los errores de autorización no exponen datos cruzados.

La prueba real de la unidad verificó aislamiento, unicidad, auditoría append-only, autorización y rollback. No se hizo merge automático: la PR queda sujeta al HITL del repositorio.
