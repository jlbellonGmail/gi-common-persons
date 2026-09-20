from pathlib import Path
import ast

def test_no_vertical_or_private_core_imports():
    for path in Path("gi_persons").glob("*.py"):
        tree=ast.parse(path.read_text(encoding="utf-8"))
        imports=[n for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
        names=[a.name for n in imports for a in getattr(n,"names",[])]
        modules=[n.module or "" for n in imports if isinstance(n,ast.ImportFrom)]
        assert not any("dental" in n.lower() or "law" in n.lower() or "crm" in n.lower() for n in names+modules)
        assert not any(x in (names+modules) for x in ["gi_platform_core.application","gi_platform_core.adapters","gi_platform_core.supabase_adapter"])

def test_migration_has_tenant_keys_and_forced_rls():
    sql=Path("supabase/migrations/20260920000100_persons.sql").read_text(encoding="utf-8").lower()
    for table in ["persons","person_identifiers","person_contacts","person_organization_links","person_audit"]:
        assert f"create table if not exists public.{table}" in sql
    assert "unique (organization_id, country_code, document_type, value_normalized)" in sql
    assert "force row level security" in sql
    assert "current_setting(''app.organization_id''" in sql
