from pathlib import Path
from importlib.metadata import version
import gi_platform_core
import gi_common_tenants

ROOT = Path(__file__).parents[1]

def test_consumed_distributions_and_public_contracts():
    assert version("gi-platform-core") == "0.3.0"
    assert version("gi-common-tenants") == "0.1.1"
    assert gi_platform_core.__version__ == "0.3.0"
    # Upstream v0.1.1 exposes a stale module __version__; Persons uses the
    # distribution metadata and records the discrepancy in its evidence.
    assert gi_common_tenants.__version__ == "0.1.0"
    from gi_platform_core import CoreApi, TENANT_CONTRACT_VERSION
    from gi_common_tenants import TenantContext
    assert CoreApi and TENANT_CONTRACT_VERSION == "0.3.0"
    assert TenantContext("u", "o").tenant_id == "o"

def test_new_schema_is_tenant_aware_and_fail_closed():
    sql = (ROOT / "supabase/migrations/20260924010000_persons_physical_and_tax.sql").read_text(encoding="utf-8")
    for table in ("person_address", "gender_option", "person_identity", "person_tax_identifier", "person_tax_profile", "tax_category"):
        assert f"create table if not exists persons.{table}" in sql
    assert "force row level security" in sql
    assert "current_setting(''app.organization_id'',true)" in sql
    assert "grant select,insert,update" in sql
