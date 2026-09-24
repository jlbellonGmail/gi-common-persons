# Contratos de integración

Todo nombre Persons de este documento es una PROPUESTA, no una API existente.
Core v0.3.0 expone CoreApi 0.1.0, identidad 0.2.0 y Tenant 0.3.0; Tenants
v0.1.1 expone TenantContext/TenantsApi públicos. Persons no accede stores.

## Core disponible

| Operación pública real | Uso previsto | Límite |
|---|---|---|
| authorize(user_id, organization_id, permission, location_id=None) | Autorizar cada caso de uso | Retorna contract_version, allowed, reason, context; no garantiza todos los flags active ni frescura |
| list_organizations(user_id) | Selector de organizaciones del actor, si el host lo necesita | Filtra membership y organización activas; no búsqueda global |
| list_memberships(user_id) | Inspección autorizada de contexto en host | Incluye inactivas; no concede permisos por existir |
| list_locations(user_id, organization_id, location_id=None) | Selector de sedes autorizadas | Requiere location:read; no es necesario para cada operación Persons |
| create_permission(code, description) | Provisioning del namespace Persons | Sin actor; sólo administración confiable |
| create_role(organization_id, name, permission_codes), assign_role(membership_id, role_id) | Administración en Core | No exponer desde Persons ni crear rol implícito |

Las otras operaciones create_organization, create_location, create_user,
add_membership y grant_location_access siguen siendo responsabilidad del host/Core.
No se invocan automáticamente al crear Person. Errores públicos observados:
CoreError, ValidationError, NotFoundError, AuthorizationError, IsolationError.

Para authorize se exige allowed booleano verdadero, versión soportada y contexto
devuelto igual al solicitado. Rechazar respuesta incompleta, incoherente o de
versión desconocida. Propuesta inicial: soportar exactamente 0.1.0; ampliar a
0.1.x sólo con prueba del contrato y compatibilidad, no por aceptar cualquier string.

## Fachada Persons propuesta

Contrato sin transporte. No se publica una URL, token, servidor ni OpenAPI real.
La versión candidata es 0.1.0-draft; una versión final requiere una unidad y
decisión de release independiente. Los nombres de métodos son diseñados aquí.

Contexto confiable: user_id, organization_id, location_id opcional y
correlation_id. El host lo construye a partir de sesión verificada; el body no
permite sobrescribir actor u organización. No almacenar credenciales en Persons.

| Operación candidata | Datos de entrada | Resultado | Permiso propuesto |
|---|---|---|---|
| create_person | context, display_name, nombres/birth_date opcionales, identificadores/contactos opcionales | PersonSummary y version; hijos atómicos | persons:write; además persons:identifier:write / persons:contact:write si incluye hijos |
| get_person | context, person_id | PersonSummary sin documentos ni contactos por defecto | persons:read |
| list_persons | context, filtros permitidos, cursor, limit | items, next_cursor; sin total global | persons:read |
| update_person | context, person_id, expected_version, campos generales permitidos | PersonSummary con nueva version | persons:write |
| list_identifiers | context, person_id | vista enmascarada; lectura completa sólo explícita y autorizada | persons:identifier:read; dato completo requiere persons:identifier:reveal |
| add_identifier | context, person_id, expected_version, país/tipo/valor | referencia identifier_id; conflicto si duplicado local | persons:identifier:write |
| list_contacts | context, person_id | contactos según alcance autorizado | persons:contact:read |
| add_contact / update_contact | context, person_id, expected_version, datos de contacto | contacto y nueva version | persons:contact:write |
| find_duplicate_candidates | context, identificadores/contactos/nombre, limit | candidatos del tenant y motivo sin PII adicional | persons:duplicates:read; filtros sensibles exigen permiso de lectura correspondiente |
| get_organization_link | context, person_id | vínculo con organización actual | persons:read |
| link_identity / unlink_identity | context, person_id, core_user_id y external_subject para validación pública | respuesta 0.2.0; idempotente | persons:identity:link / persons:identity:unlink; Core aplica permisos equivalentes |

Los permisos son códigos candidatos compatibles con el formato namespace:acción
de Core, no permisos existentes. Validar su formato con el Core real en U02.
No exponer un endpoint administrativo para que el solicitante se los otorgue.

PersonSummary: contract_version, organization_id, person_id, display_name,
given_names/family_names/birth_date opcionales, status, version, created_at,
updated_at. No incorporar core_user_id, identificadores ni contactos por defecto.
La exposición de birth_date puede restringirse adicionalmente según política
de PII acordada. No devolver entidades Python privadas ni estructuras de stores.

PATCH conceptual: campos omitidos se conservan; null limpia sólo opcionales;
campos desconocidos e IDs inmutables se rechazan. expected_version es obligatorio
en toda mutación de agregado existente, también hijos y enlace Identity.

Listados: limit default 20, máximo propuesto 100; orden estable por person_id;
cursor opaco ligado a tenant, filtros y orden. Reautorizar cada página. No
incorporar PII en el cursor ni permitir reutilizarlo en otro tenant. No prometer
snapshot consistente de varias páginas sin un contrato explícito.

Errores candidatos: VALIDATION_ERROR, NOT_FOUND, FORBIDDEN, DUPLICATE_IDENTIFIER,
VERSION_CONFLICT, CORE_UNAVAILABLE, UNSUPPORTED_CORE_CONTRACT,
CAPABILITY_UNAVAILABLE. Nunca devolver reason de Core sin sanear ni datos de
otro tenant. Si más adelante existe HTTP: 400/404/403/409/503 según categoría,
autenticación 401 a cargo del host; esto no constituye endpoint implementado.

Un ID fuera del tenant se responde NOT_FOUND después de autorizar al actor para
la operación local. No acceder a otro tenant para distinguirlo. Conflicto de
documento no devuelve Person sin permiso de lectura; candidato sólo por consulta
autorizada. Logs no guardan documento original ni request body completo.

Reintentos de creación sin identificador pueden duplicar personas: no prometer
exactly-once. Antes de habilitar transporte con reintentos, añadir contrato de
idempotencia por (organization_id, actor, operación, key), hash de request sin
PII expuesta y política de retención; nueva autorización aun en replay. Esa
política se decide en U06. Un timeout no autoriza a repetir una mutación a ciegas.

## Dependencias y posibles cambios en Core (NO implementados)

| ID | Necesidad | Alternativa y alcance | Bloquea |
|---|---|---|---|
| D1 | Resolver sujeto autenticado y validar identidad destino sin APIs privadas | Resuelto por CoreApi identidad 0.2.0 y RequestContext confiable del host | — |
| D2 | Estados active de user/org/location/role/permission y revocaciones frescas | Corregir proveedor + contrato de frescura/revocación. Instancia por request sólo mitiga snapshot; no corrige flags omitidos | Habilitación productiva de autorización |
| D3 | Auditoría de dominio interoperable | Eventos propios transaccionales Persons; si se exige colector común, contrato público separado. No usar CoreStore/AuditSink internos | Colector central, no necesariamente persistencia local de trazas |
| D4 | Contrato seguro de persistencia/RLS | Contexto de DB resuelto por host sin tabla privada; validar rol y pool. Core RLS no cubre Persons | Adaptador productivo/U05 |
| D5 | Payloads y compatibilidad de Core formalizados | Pruebas de consumidor sobre CoreApi actual; proponer schema público si GI lo necesita | No bloquea diseñar; sí impide afirmar validación completa por el schema actual |

Cambios D1/D2/D3 en Core requieren alcance, pruebas de regresión, compatibilidad,
impacto en consumidores y autorización específica antes de tocar ese repo.
Persons no los resuelve agregando tablas espejo ni un segundo motor de permisos.
No hay transacción pública distribuida Core–Persons; autorización y commit local
son pasos separados, con riesgo temporal que el contrato de revocación debe acotar.
