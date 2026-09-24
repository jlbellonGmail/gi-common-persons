# Decisiones

- Se conserva `Person ↔ Identity` local como referencia opaca y se valida la
  identidad mediante `CoreApi.validate_identity`/`link_identity`; Persons no
  crea usuarios ni replica membership.
- Se agrega `gi-common-tenants==0.1.1` sólo como dependencia de contrato; no
  se consulta ninguna tabla privada de Tenants.
- La ausencia de publicación PyPI impide validar una instalación desde índice;
  se ejecutará además una instalación limpia desde los tags locales como
  evidencia separada, sin presentarla como disponibilidad pública.
