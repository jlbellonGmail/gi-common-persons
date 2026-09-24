"""Public compatibility constants for the published Core/Tenants contracts."""
CORE_PACKAGE = "gi-platform-core==0.3.0"
TENANTS_PACKAGE = "gi-common-tenants==0.1.1"
CORE_AUTHORIZATION_CONTRACT = "0.1.0"
CORE_IDENTITY_CONTRACT = "0.2.0"
CORE_TENANT_CONTRACT = "0.3.0"

def tenant_context(user_id: str, organization_id: str):
    """Build the public Tenants context without touching its private stores."""
    from gi_common_tenants import TenantContext
    return TenantContext(user_id, organization_id)
