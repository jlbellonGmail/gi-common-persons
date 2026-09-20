# Inspección previa — 2026-09-20

## Alcance y fuentes

Se recuperó la conversación completa «Diseño módulo Personas»
`6aaf5470-5f9c-83e9-9f8f-354b1d46bcd0`, incluidos los apartados 3–8 que no
aparecían completos en el preview. Se inspeccionaron archivos locales, Git y
consultas read-only de GitHub. No se ejecutaron cambios en los proveedores.

## Repositorios y releases

| Fuente | Evidencia observada | Interpretación |
|---|---|---|
| C:\Proyectos\gi-platform-core | develop limpio; HEAD/tag v0.1.0 `673a9a80ff436171e8138aaaa0da4dd96f190d8e` | Baseline Core examinada |
| Core main local | `6a9cc23`, inicialización | No confundir main con la release real |
| Core GitHub | release v0.1.0 publicada 2026-09-19T22:39:04Z; no draft/prerelease; targetCommitish develop | Release existente; no se corrige su gobernanza desde Persons |
| Core objeto anotado | `55755c5e02dd9a0beb62274a5ba2a373d5042563` | Mantener objeto y commit; no retag |
| C:\Proyectos\template | checkout limpio maintenance/status-v2.0.1-final, HEAD `ff89cf7f3e2d54717b70cc253810db119eccd629` | No usar ciegamente HEAD como baseline |
| Template release v2.0.1 | commit `fa8aade44fe808635e01916da7347b1d1837da7a`; objeto anotado `e1e032c1ef6414fd701a41d3062f9dcd58f425c3` | Baseline elegida y archivada desde el tag |
| Template GitHub | release publicada 2026-09-18T19:13:49Z; CI del commit fa8aade success; PR 112 abierta y CI ff89cf7 failure | Snapshot del tag, no la rama de mantenimiento |
| Persons local | No encontrado en enumeración de C:\Proyectos y búsqueda recursiva por nombre | Bootstrap nuevo; no prueba inexistencia en todo el equipo |
| Persons remoto | repo view jlbellonGmail/gi-common-persons no resuelve; listado visible sin coincidencias person | No se afirma inexistencia en otras cuentas o repos privados no accesibles |
| D:\proyectos | Sin unidad D disponible en Get-PSDrive de esta sesión | Usar C:\Proyectos |

Core: PR 1, 2 y 4 figuran MERGED. El run «Publish Core package» sobre
673a9a8 figura success. El CI observado sobre 9ddad68 figura success; no se
afirma que ese run sea CI del SHA de release. No se reejecutó la suite de Core.

La release adjunta `gi_platform_core-0.1.0-py3-none-any.whl`, digest publicado
`sha256:9a8c4cf65d5577e641c2d4cc9de3f9cc37a0e7961910b6f221549b2e52c25536`.
Se inspeccionó metadata, no se descargó ni verificó el contenido del wheel.

## Superficie pública realmente observada

Fuentes relativas a Core: `docs/tecnica/core-contract-v010.md`,
`contracts/core-api-v0.1.0.manifest.json`, `gi_platform_core/contracts.py`,
`errors.py`, `application.py`, `authorization.py`, `ports.py`,
`supabase_adapter.py`, documentación técnica y pruebas.

Core expone CoreApi, valores JSON y excepciones públicas. No habilita importar
entidades privadas, stores, TenantContext ni consultar tablas desde Persons.
El manifiesto contiene 12 operaciones. Su JSON Schema valida el manifiesto;
no es OpenAPI ni un schema exhaustivo de payloads de cada operación.

Se reutilizan authorize y, cuando la operación lo requiera, list_organizations,
list_memberships y list_locations. Las operaciones create_permission y
create_role existen para provisioning confiable, no para exponerlas al usuario
final desde Persons. El host conserva composición, autenticación y sesión.

No existen en CoreApi operaciones públicas para resolver external_subject,
consultar identidad destino, revocar estados o recibir eventos de auditoría de
Persons. AuditSink/CoreStore son interfaces internas, no contratos públicos
autorizados para el consumidor. No se inventa un endpoint que las reemplace.

## Desvíos y dependencias

- STATUS de Core declara HEAD 740b23ad y árbol dirty; Git muestra 673a9a8 y árbol limpio.
- ROADMAP conserva 01 en READY_FOR_PR pese a existir release. No se infiere cierre de esa unidad.
- Arquitectura histórica dice persistencia futura; hay adaptador y migración Supabase. Verificar código y evidencia por encima de ese resumen.
- authorize verifica membership activa, roles, pertenencia de location y acceso asignado; no verifica todos los flags active de usuario/organización/sede.
- El adaptador carga estado en memoria; una revocación externa puede no verse sin renovación. No prometer revocación inmediata.
- Los métodos administrativos públicos no reciben actor/contexto: deben quedar en provisioning confiable.
- El updater STATUS del Template conserva una versión fija v2.0.0: registrar la discrepancia, no presentar esa cadena como versión de Persons.

Estos hallazgos son insumos de diseño, no autorizaciones para modificar Core ni
Template. El detalle de impacto y alternativas está en contratos-persons.md.

## Límites de verificación

Las primeras consultas GitHub fallaron por acceso a configuración del CLI en el
sandbox; se repitieron con elevación autorizada y lectura solamente. Git se
consultó con safe.directory por invocación, sin cambiar configuración global.
No se inspeccionaron secretos .env, tenants reales, datos personales ni tablas
remotas. No se modificaron verticales ni se inspeccionó su implementación.
