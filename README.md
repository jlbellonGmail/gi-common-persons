# GI-COMMON-PERSONS

Fundación documental de la capacidad común de personas físicas de GI.
No hay implementación funcional, API desplegada ni release de Persons.

- [Estado verificable](STATUS.md).
- [Hallazgos y procedencia](docs/tecnica/inspeccion-fundacion.md).
- [Arquitectura y decisiones](docs/tecnica/arquitectura-persons.md).
- [Modelo de datos propuesto](docs/tecnica/modelo-persons.md).
- [Contratos propuestos y dependencias reales](docs/tecnica/contratos-persons.md).
- [Unidades de trabajo, pruebas y gates](docs/tecnica/plan-persons.md).

El circuito procede de Template GI v2.0.1, commit
`fa8aade44fe808635e01916da7347b1d1837da7a`, como snapshot independiente.
Sus documentos históricos explican el circuito; no prueban funcionalidades,
auditorías ni releases de este proyecto. No se importan runs históricos.

Core inspeccionado: v0.1.0, commit
`673a9a80ff436171e8138aaaa0da4dd96f190d8e`.
La dependencia es Persons → Core; las verticales consumen Persons.

Este bootstrap local todavía no constituye una work unit cerrada por el
circuito. No existe remoto confirmado para Persons. Su publicación, CI y PR
quedan pendientes; no se simulan con un remoto local ni con aprobaciones ficticias.
