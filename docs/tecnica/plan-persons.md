# Plan de unidades de trabajo

Diseño inicial primero. El bootstrap local no sustituye identidad de work unit,
ASSESS, review, PR ni HITL. Ninguna unidad se marca completada por redactarla.

## Adopción del Template

Baseline: tag v2.0.1 / commit fa8aade44fe808635e01916da7347b1d1837da7a.
Copiar circuito y tests como snapshot, adaptar identidad del proyecto y conservar
procedencia. No copiar runs/auditorías completadas/roadmap de Template como
evidencia de Persons. Regenerar adaptadores sólo desde .agentic si cambia esa
fuente. No modificar adaptadores generados a mano.

Repositorio remoto no identificado: preparar bootstrap local sin inventar
origin ni crear un repositorio público. start-work-unit.ps1 hace fetch origin
develop y exige baseline limpia: no fabricar manifiesto para evitar ese gate.
Tras resolver remoto y baseline, iniciar 01 desde develop por el script oficial.
No crear main, tag o release automáticamente. El bootstrap usa rama codex propia;
las unidades usarán los nombres feature/ que produce el contrato del Template.

## Descomposición y aceptación

| Unidad | Dependencias | Alcance y aceptación comprobable |
|---|---|---|
| U01 / 01-fundacion-diseno | remoto para circuito completo; decisión P01 | Arquitectura, modelo, contratos propuestos, límites, trazabilidad y decisiones resueltas para la unidad; reviewer independiente y adopción sin historia falsa |
| U02 / 02-contrato-core | U01; D1/D2 para integración real | Pin proveedor, pruebas a CoreApi/errores/JSON; no imports internos. Falla cerrada con versión desconocida y respuesta incoherente. Registrar gaps sin modificar proveedor |
| U03 / 03-personas-identificadores | U01, catálogo documental confirmado | Agregado y reglas deterministas; persona sin documentos válida; unicidad por tenant/país/tipo; conflicto concurrente previsto. Pruebas puras con puerto, no producción |
| U04 / 04-contactos-vinculos | U03; D1 sólo para Identity | Contactos compartidos permitidos, primary único, vínculo propio sin membership; dejar enlace Identity en unidad separada si D1 sigue abierto |
| U05 / 05-persistencia-aislamiento | U02/U03/U04; D2/D4 | Migraciones de Persons y adaptador; pruebas DB reales cross-tenant, rollback, versiones, carreras y auditoría. No usar gi-dev sin spec/destino/autorización |
| U06 / 06-api-publica | U02–U05 | Fachada, schema público propio, permisos, errores sanitizados, cursor tenant-aware y política de idempotencia antes de reintentos. HTTP sólo si una necesidad concreta lo autoriza |
| U07 / 07-readiness-integracion | U06, decisiones de privacidad | CI del SHA vigente, empaquetado reproducible, pruebas consumidor sin verticales reales, revisión/auditoría y PR lista para MERGE/NO MERGE |

U02 y el diseño de U03 pueden avanzar independientemente tras U01. No agrupar
todo en un milestone: sus decisiones y criterios pueden revisarse por separado.
No implementar un bloqueo de Core dentro de Persons para aparentar cierre.

## Matriz mínima de pruebas

| Requisito | Casos de prueba antes de habilitarlo |
|---|---|
| Límites de módulos | Imports de producto sólo CoreApi/errores; ninguna dependencia vertical ni SQL Core; consumidor sintético por fachada |
| Tenant | A no lee/actualiza/lista/cuenta/candidatea IDs de B; mismo documento válido en A/B; FK compuesta impide hijo de B en A; body/cursor no alteran tenant |
| Identity | Person sin cuenta; enlace no crea cuenta/membership; destino inexistente/inactivo o no probado se rechaza; enlace duplicado local entra en conflicto; unlink conserva Person |
| Autorización | Sin membership/permission, membership inactiva, sede ajena/no concedida, todos los flags activos, revocación durante vida del proceso, proveedor caído/response mal formada/version mismatch |
| Identificadores | Catálogo y normalización por país/tipo, ceros significativos, colisiones y migración de versión; dos transacciones simultáneas, rollback sin huérfanos |
| Contactos | Email/teléfono compartidos entre personas; no transformación destructiva; primary concurrente; cliente no marca verificado |
| Versionado | Dos updates con misma versión: uno gana y otro conflicto; hijos incrementan versión; parche sólo de campos permitidos |
| Auditoría | Una mutación y evento atómicos; fallo sink revierte; redacción de PII; denegación sin fuga; log append-only |
| Persistencia | Pruebas con roles auténticos del adaptador, RLS si se declara, sin bypass, conexión reutilizada entre tenants; rollback migración según estrategia |
| Contrato | JSON-safe, campos requeridos, errores, compatibilidad, paginación estable; no confundir manifiesto Core con schema de payload |
| Operación | Reintentos con política acordada, fallos parciales, límites de entrada, instalación del paquete y hash de dependencia |

## SDD, QA, CI y HITL

1. Ejecutar scripts/assess-work-unit.ps1 con rutas reales del diff y conservar
   JSONL; materialize-sdd.ps1 deriva LIGHT/STANDARD/FULL. No clasificar a mano.
2. Planner produce intención/plan según salida, separa hechos y supuestos,
   aplica CLARIFY sólo a decisiones materiales. Reviewer rechaza spec bloqueada.
3. Builder implementa sólo alcance habilitado. QA ejecuta pruebas relevantes de
   producto, suite del circuito, contratos e índices. Evidencia real en runs.
4. Reviewer revisa diff final y SHA vigentes. Cada cambio posterior invalida
   verificaciones afectadas; no reutilizar un approved de otro estado.
5. Con gates locales/review aprobados, ready-for-pr.ps1 → [-] READY_FOR_PR;
   publicar rama/PR develop y wait-pr-ci.ps1. No pedir HITL sobre un documento
   abstracto ni marcar CI verde por el placeholder product-tests.
6. Único HITL de merge: humano decide MERGE/NO MERGE sobre PR real y CI verde.
   complete-approved-pr.ps1 sólo con esa decisión; close-feature.ps1 confirma
   merge y recién entonces [x]. Tags/releases requieren decisión separada.

CI heredada exige circuit-tests, product-tests y local-reconciler-tests. Durante
bootstrap sin producto, product-tests sigue explícitamente placeholder; U03/U05
deben sustituirlo por pruebas reales antes de afirmar cobertura de producto.
No usar continue-on-error ni esquivar tests fallidos. Integración DB/contratos y
build del paquete se agregan según stack elegido, sin credenciales productivas.

Auditoría: conservar evidencia de riesgos/decisiones, no inventar score 100/100.
Seleccionar perfil .audit realmente activo antes de puntuar una biblioteca;
un perfil LIBRARY marcado NO IMPLEMENTADO no sirve como gate operativo.

## Clarificaciones materiales pendientes

- P01 RESUELTA el 2026-09-20: por organización, sin compartir entre tenants.
- Identity: cardinalidad y evidencia de titularidad/actuación autorizada; host real.
- Países/tipos documentales iniciales; retención, borrado y exposición de PII.
- Remoto propietario/visibilidad; entorno real de persistencia cuando corresponda.

Estas cuestiones se resuelven en la unidad que dependa de ellas, sin frenar
documentación y pruebas sintéticas independientes. No se solicita autorización
para modificar Core en esta fundación: sólo se registran impactos candidatos.
