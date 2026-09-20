from pathlib import Path
import ast


def test_no_vertical_or_private_core_imports():
    for path in Path("gi_persons").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
        names = [alias.name for node in imports for alias in getattr(node, "names", [])]
        modules = [node.module or "" for node in imports if isinstance(node, ast.ImportFrom)]
        assert not any(name.lower() in {"dental", "law", "crm"} for name in names + modules)
        assert not any(
            name in {"gi_platform_core.application", "gi_platform_core.adapters", "gi_platform_core.supabase_adapter"}
            for name in names + modules
        )


def test_migration_has_persons_schema_tenant_keys_and_forced_rls():
    sql = Path("supabase/migrations/20260920000100_persons.sql").read_text(encoding="utf-8").lower()
    for table in ["person", "person_identifier", "person_contact", "person_organization_link", "person_audit"]:
        assert f"create table if not exists persons.{table}" in sql
    assert "unique (organization_id, country_code, document_type, value_normalized)" in sql
    assert "force row level security" in sql
    assert "current_setting(''app.organization_id''" in sql
