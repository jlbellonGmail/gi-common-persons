status: approved
La CLI mantiene un bloqueo de transporte contra `api.supabase.com`, documentado en `deployment-attempt.json`. La alternativa fue la API autenticada para obtener un login role temporal y el pooler PostgreSQL regional; el secreto se mantuvo sólo en memoria. El despliegue, la introspección y la prueba real fueron completados sin modificar Core ni verticales.
