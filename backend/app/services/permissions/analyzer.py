from typing import List, Dict, Set
from ...graph.database import get_db_connection
from .policy_parser import AWSPolicyParser
from ..models.event import EffectivePermissionSummary

class EffectivePermissionAnalyzer:
    def __init__(self):
        self.db = get_db_connection()

    def analyze_identity(self, identity_id: str, observed_events: List[str]) -> EffectivePermissionSummary:
        """
        Compare observed usage against granted permissions
        """
        granted_actions = self._get_granted_actions(identity_id)
        used_actions = set(observed_events)
        
        # Simple intersection/delta
        # In reality, we handle wildcards and NotAction
        granted_set = set(granted_actions)
        
        unused_actions = list(granted_set - used_actions)
        
        return EffectivePermissionSummary(
            identity_id=identity_id,
            granted_count=len(granted_set),
            used_count=len(used_actions),
            over_permissive_count=len(unused_actions),
            unused_actions=unused_actions,
            used_actions=list(used_actions)
        )

    def _get_granted_actions(self, identity_id: str) -> List[str]:
        driver = self.db.get_driver()
        actions = []
        
        with driver.session() as session:
            # Query all policies attached to identity or its groups
            query = """
            MATCH (i:Identity {id: $id})
            OPTIONAL MATCH (i)-[:ATTACHED_POLICY]->(p:Policy)
            OPTIONAL MATCH (i)-[:MEMBER_OF]->(g:Identity)-[:ATTACHED_POLICY]->(gp:Policy)
            RETURN p.document as direct_doc, gp.document as group_doc
            """
            result = session.run(query, id=identity_id)
            for record in result:
                for key in ['direct_doc', 'group_doc']:
                    doc_str = record[key]
                    if doc_str:
                        import json
                        try:
                            doc = json.loads(doc_str)
                            actions.extend(AWSPolicyParser.get_actions_from_policy(doc))
                        except:
                            pass
        return list(set(actions))

    def update_graph_with_usage(self, summary: EffectivePermissionSummary):
        """Store effective permission metadata back into Neo4j"""
        driver = self.db.get_driver()
        with driver.session() as session:
            session.run("""
                MATCH (i:Identity {id: $id})
                SET i.used_permissions = $used,
                    i.unused_permissions = $unused,
                    i.risk_score = $risk
            """, 
            id=summary.identity_id, 
            used=summary.used_actions, 
            unused=summary.unused_actions,
            risk=min(1.0, summary.over_permissive_count / max(1, summary.granted_count))
            )
