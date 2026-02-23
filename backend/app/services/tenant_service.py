from typing import List, Dict, Any
from ..models.tenant import Tenant, RiskSnapshot
from ..graph.database import get_db_connection

def get_tenant_risk_summary(tenant_id: str) -> RiskSnapshot:
    """Computes a high-level risk summary for the SaaS dashboard"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        # Total Identities and High Risk Count
        # In a real multi-tenant setup, we'd filter by tenant_id
        res = session.run("""
            MATCH (i:Identity)
            WITH count(i) as total
            MATCH (hr:Identity) WHERE hr.high_privilege = true OR hr.risk_score > 0.7
            WITH total, count(hr) as high_risk
            MATCH (a:Alert)
            RETURN total, high_risk, count(a) as alerts
        """)
        record = res.single()
        
        # Calculate over-permissiveness
        usage_res = session.run("""
            MATCH (i:Identity)
            WHERE i.used_permissions IS NOT NULL
            RETURN avg(size(i.unused_permissions) * 1.0 / (size(i.used_permissions) + size(i.unused_permissions))) as avg_unused
        """)
        usage_record = usage_res.single()
        avg_unused = usage_record['avg_unused'] or 0

        return RiskSnapshot(
            total_identities=record['total'],
            high_risk_count=record['high_risk'],
            over_permissive_percent=avg_unused * 100,
            recent_alerts_count=record['alerts']
        )
