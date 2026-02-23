from typing import List, Dict, Any
from ...models.guard import ProposedChange
from ...services.identity_service import get_identity_by_id

class FeatureExtractor:
    """Prepares feature vectors for the Predictive Risk Engine (Phase 3.5 Ready)"""

    @staticmethod
    def extract_features(change: ProposedChange, introduces_escalation: bool, rule_score: float) -> Dict[str, Any]:
        """
        Transforms a proposed change into a feature vector.
        Features include:
        - Permission counts (total, sensitive, wildcards)
        - Graph context (identity centrality placeholder)
        - Action density
        - Escalation binary
        """
        features = {}

        # 1. Structural Features
        features["num_added_permissions"] = len(change.added_permissions)
        features["num_removed_permissions"] = len(change.removed_permissions)
        features["is_wildcard_resource"] = 1 if change.resource_scope == "*" else 0
        features["is_escalation"] = 1 if introduces_escalation else 0
        
        # 2. Sensitivity Features
        sensitive_count = 0
        wildcard_action_count = 0
        for action in change.added_permissions:
            if "*" in action:
                wildcard_action_count += 1
            if any(s in action for s in ["Admin", "Policy", "Role", "Secret", "Key"]):
                sensitive_count += 1
        
        features["sensitive_action_ratio"] = sensitive_count / max(1, len(change.added_permissions))
        features["wildcard_action_ratio"] = wildcard_action_count / max(1, len(change.added_permissions))

        # 3. Contextual Features (Identity Graph)
        # In a real setup, we'd query graph centrality (Pagerank/Betweenness)
        # For MVP, we use the identity type as a proxy
        type_map = {"user": 1.0, "role": 1.5, "group": 1.2, "policy": 0.5}
        features["identity_type_weight"] = type_map.get(change.identity_type.lower(), 1.0)
        
        # 4. Rule Engine Fallback
        features["rule_engine_baseline"] = rule_score

        return features
