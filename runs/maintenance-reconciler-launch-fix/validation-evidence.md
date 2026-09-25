# Evidencia — corrección del launcher del reconciliador

Fecha: 2026-09-25

- Causa reproducida: `scripts/local-feature-reconcile.ps1` usaba
  `$scriptPath` sin inicializar al construir `Start-Process`. El hijo recibía
  `-File -Slug` y Windows registraba `Error al procesar -File '-Slug'`.
- Corrección: resolver `$scriptPath` desde `$PSCommandPath` y fallar cerrado si
  la ruta no existe. No se modificaron timeouts ni se ocultaron errores.
- Prueba puntual local: `test_start_reconciler_from_linked_worktree` pasó.
- El conjunto completo del reconciliador se ejecutará en CI sobre esta rama;
  el fallo previo afectaba ese test y los otros seis tests pasaban.
