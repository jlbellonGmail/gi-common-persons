# Validation evidence

- `pip index versions gi-platform-core`: no matching distribution.
- `pip index versions gi-common-tenants`: no matching distribution.
- Exact local tags verified: Core `v0.3.0` at `6b10d564a5ce96065f87a44d6ddbd58ec5342500`; Tenants `v0.1.1` at `8af783f8b84fafc2629afc293b16fae835b828fe`.
- Local editable distribution metadata: Core `0.3.0`, Tenants `0.1.1`.
- Module metadata: Core `__version__ == 0.3.0`; Tenants `__version__ == 0.1.0` (upstream mismatch).
- Persons tests: `24 passed, 1 skipped` (real Supabase credentials absent).
- Core integration: `4 passed`.
- Full pytest command completed successfully; the circuit suite is included by the repository pytest configuration.
- No real Supabase migration was executed: `PERSONS_TEST_DATABASE_URL` absent. The migration contract test passed and no deployment was attempted.
