# Spec — persistencia Supabase real

## Hechos verificados

- El proyecto Supabase vinculado es `gletzbwuvmwjkmoufmyj` (`gi-dev`).
- La migración anterior estaba en `public`, con nombres de tablas incompatibles y SQL truncado.
- El alcance exige el esquema `persons`, cinco tablas, aislamiento por `organization_id`, claves tenant-aware, índices y RLS.
- No se modifica Core ni ninguna vertical.

## Decisiones

- `organization_id` forma parte de las claves primarias y de todas las FK internas.
- La política RLS usa `current_setting('app.organization_id', true)` y se aplica con `FORCE ROW LEVEL SECURITY`.
- El audit es insert-only para el rol de aplicación: no recibe grants de UPDATE/DELETE ni políticas de escritura mutadora.
- La prueba real usa una transacción que termina en rollback y el rol `authenticated`, nunca `service_role`.

## Bloqueo actual

La CLI autenticada `2.117.0` no logra completar `db push`: el endpoint de Supabase responde `TransportError` al solicitar el login role. Sin ese paso no se puede afirmar aplicación, existencia remota, RLS efectivo ni aislamiento real.
