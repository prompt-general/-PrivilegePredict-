from typing import List, Dict, Any
from ...models.guard import ProposedChange

class RiskScoringEngine:
    """Rule-based risk scoring for proposed IAM changes"""

    SENSITIVE_ACTIONS = {
        "iam:PassRole": 40,
        "sts:AssumeRole": 35,
        "iam:CreateAccessKey": 30,
        "iam:PutRolePolicy": 45,
        "iam:AttachRolePolicy": 45,
        "iam:UpdateAssumeRolePolicy": 50,
        "*": 100,
        "*:*": 100,
        "s3:PutBucketPolicy": 20,
        "lambda:UpdateFunctionCode": 25
    }

    def compute_score(self, change: ProposedChange, introduces_escalation: bool) -> float:
        score = 0.0
        
        # 1. Action sensitivity
        for action in change.added_permissions:
            # check direct match
            if action in self.SENSITIVE_ACTIONS:
                score += self.SENSITIVE_ACTIONS[action]
            # check wildcard match (e.g. iam:*)
            elif ":" in action:
                prefix = action.split(":")[0] + ":*"
                if prefix in self.SENSITIVE_ACTIONS:
                    score += self.SENSITIVE_ACTIONS[prefix] * 0.8 # slightly lower for prefix wildcards
            elif action == "*":
                 score += 100

        # 2. Escalation Path Penalty
        if introduces_escalation:
            score += 60 # Increased penalty 

        # 3. Resource Scope Penalty
        if change.resource_scope == "*":
            score += 15 # Flat penalty for wildcards
            
        # 4. Cross-Account / Extra-Trust detection
        if self._is_trust_change(change):
            score += 30

        return min(100.0, score)

    def get_reasons(self, change: ProposedChange, introduces_escalation: bool) -> List[str]:
        reasons = []
        score = self.compute_score(change, introduces_escalation)

        if introduces_escalation:
            reasons.append("Proposed changes introduce a new privilege escalation path to administrative access.")
        
        for action in change.added_permissions:
            if action in self.SENSITIVE_ACTIONS and self.SENSITIVE_ACTIONS[action] >= 30:
                reasons.append(f"Adding highly sensitive permission: {action}")
            elif action == "*" or action == "*:*":
                reasons.append("Adding full administrative wildcards (*).")

        if change.resource_scope == "*" and score > 30: 
             reasons.append("Permissions are scoped to all resources ('*'), increasing blast radius.")
             
        if self._is_trust_change(change):
            reasons.append("Change modifies identity trust relationships (e.g. AssumeRolePolicy), potentially allowing cross-account access.")

        return reasons

    def _is_trust_change(self, change: ProposedChange) -> bool:
        """Detects if the change modifies trust/resource policies"""
        trust_actions = ["iam:UpdateAssumeRolePolicy", "iam:CreateOpenIDConnectProvider", "iam:CreateSAMLProvider"]
        return any(a in change.added_permissions for a in trust_actions)

