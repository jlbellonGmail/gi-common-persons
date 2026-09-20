# Modelo de datos propuesto

Diseño lógico, no DDL aplicado. Depende de ADR-P01 por organización. UUIDs opacos
generados server-side; fechas/hora UTC; las fechas civiles usan date. No asumir
que un documento o contacto identifica globalmente a una persona.

## Entidades y claves

| Entidad | Atributos propuestos | Claves y restricciones |
|---|---|---|
| Person | person_id, organization_id, display_name, given_names opcional, family_names opcional, birth_date opcional, status active/archived, version, created_at/by, updated_at/by | PK person_id; UNIQUE(organization_id, person_id); display_name no vacío; version positiva; organización inmutable |
| PersonIdentifier | identifier_id, organization_id, person_id, country_code, document_type, value_original protegido, value_normalized protegido, normalization_version, created_at/by | PK identifier_id; FK compuesta (organization_id, person_id) → Person; UNIQUE(organization_id, country_code, document_type, value_normalized) |
| PersonContact | contact_id, organization_id, person_id, kind email/phone, value_original, value_normalized, label opcional, is_primary, verified_at opcional, created_at/by, updated_at/by | PK contact_id; FK compuesta a Person; UNIQUE(organization_id, person_id, kind, value_normalized); índice único parcial de primary por (organization_id, person_id, kind) |
| PersonOrganizationLink | link_id, organization_id, person_id, status active/inactive, created_at/by, ended_at opcional | PK link_id; FK compuesta a Person; UNIQUE(organization_id, person_id); sólo organización propietaria en esta etapa |
| PersonIdentityLink | link_id, organization_id, person_id, core_user_id, linked_at/by | PK link_id; FK compuesta a Person; UNIQUE(organization_id, person_id) y UNIQUE(organization_id, core_user_id), cardinalidad inicial propuesta 0..1 |
| PersonAudit | audit_id, organization_id, person_id opcional, action, actor_user_id, occurred_at, correlation_id, outcome, entity_version | append-only; escritura transaccional; sin PII en payloads |

Core user_id/organization_id son referencias opacas externas. No se crean FK
hacia tablas privadas de Core ni copia de sus catálogos/membresías. Tipos físicos
UUID sólo si el contrato de proveedor los garantiza; la API actual usa strings.
Las FK compuestas internas impiden colgar un contacto/documento del tenant A de
una Person del B. Nunca usar sólo person_id para consultas de negocio.

PersonOrganizationLink expresa pertenencia del registro, no permiso de acceso,
especialidad ni membership. Su fila se crea atómicamente con Person. Es una
relación 1:1 inicial, explícita para no prometer muchos tenants; podría derivarse
de Person en una primera implementación más pequeña si se conserva el contrato.
No activar otra organización ni transferir organization_id con un update.

## Datos generales

Aceptar nombres monónimos y no inferir nombre/apellido desde display_name.
No imponer DNI, fecha de nacimiento, sexo, nacionalidad o cuenta de acceso para
crear Person. No introducir atributos sensibles sin necesidad confirmada.
Propuesta: nombres hasta 200 caracteres, contactos hasta 254/email y límite
definido para teléfono, paginación acotada; límites finales versionados en spec.
Fecha de nacimiento futura es inválida; no calcular ni persistir edad.

## Identificadores y deduplicación

country_code identifica país emisor (ISO alpha-2), no residencia. document_type
pertenece a un catálogo explícito por país con normalizador versionado; el set
inicial está pendiente. Sin regla confirmada, rechazar ese tipo en vez de
remover caracteres o ceros de forma destructiva. Pasaporte y documentos
renovables requieren una regla específica antes de su habilitación.

La clave única es por tenant, país, tipo y valor normalizado. Conservar ceros
significativos. No usar nombre/fecha de nacimiento como UNIQUE. Email y teléfono
pueden ser compartidos por familiares y no son únicos por tenant. Una persona
sin documentos es válida; su creación no garantiza ausencia de duplicados.

Flujo propuesto: autorizar → normalizar → candidatos sólo en tenant → insertar
en transacción. La restricción DB resuelve carreras: dos altas simultáneas con
la misma clave producen una creación y un conflicto, sin agregados huérfanos.
El precheck no reemplaza esa restricción. El conflicto no expone otra organización.

Coincidencia exacta de documento normalizado bloquea duplicación local. Nombres,
contactos y nacimiento generan candidatos explicables; nunca fusión automática
ni bloqueo por un puntaje opaco. No usar IA para decidir identidad. Búsqueda y
candidatos necesitan permisos independientes, límites y auditoría sin PII.

Archivar Person no libera sus documentos: permite detectar el registro previo.
Retirar/corregir identificadores y permitir reutilización exige un flujo
auditado con política explícita; no se implementa delete/reasignación en la
primera API. Un futuro cambio de normalizador requiere detectar colisiones y
un plan de migración reversible, no reescribir claves en caliente.

## Contactos y vínculo Identity

Email: trim, normalización del dominio; no quitar puntos ni aliases del local
part. Teléfono: E.164 únicamente con prefijo/país explícito; sin inferir país
por tenant. verified_at sólo se establece por verificación confiable futura,
nunca por un booleano del cliente. Contacto no demuestra titularidad de Identity.

Enlace Identity es opcional y autorizado; Person sigue existiendo al quitarlo.
No enlazar por coincidencia de email/documento, ni crear membership al enlazar.
Antes de habilitarlo: definir cardinalidad, prueba de titularidad/actuación
administrativa y contrato de validación de identidad en Core/host. La API de
enlace permanece fuera de capacidades habilitadas mientras falte esa dependencia.
La unicidad es tenant-aware: un usuario de Core con acceso a dos organizaciones
puede tener un enlace independiente en cada una, sin compartir datos personales.

## Concurrencia y persistencia

Updates requieren expected_version; mismatch produce conflicto y no pisa
cambios concurrentes. Cada mutación incrementa versión del agregado, incluidos
contactos/identificadores/vínculos, y confirma auditoría en la misma transacción.

Índices por (organization_id, status, person_id), claves documentales y contactos
normalizados permiten consultas acotadas. No exponer índices globales a consultas.
RLS sería defensa adicional al servicio: antes de elegir Supabase se debe
resolver un contexto DB confiable sin consultar tablas privadas de Core, roles
sin bypass, limpieza de contexto en pool y pruebas autenticadas cross-tenant.
Si sólo hay service_role privilegiado, no afirmar aislamiento DB efectivo.
