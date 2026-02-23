import json
from typing import List, Dict, Any

class AWSPolicyParser:
    """Simplified AWS IAM Policy Parser"""
    
    @staticmethod
    def get_actions_from_policy(policy_doc: Dict) -> List[str]:
        actions = []
        statements = policy_doc.get('Statement', [])
        if isinstance(statements, dict):
            statements = [statements]
            
        for statement in statements:
            if statement.get('Effect') == 'Allow':
                action_field = statement.get('Action', [])
                if isinstance(action_field, str):
                    actions.append(action_field)
                else:
                    actions.extend(action_field)
        return list(set(actions))

    @staticmethod
    def expand_wildcards(actions: List[str], all_available_actions: List[str]) -> List[str]:
        """
        Placeholder for wildcard expansion.
        In a real scenario, 's3:*' would be expanded to all S3 actions.
        """
        expanded = []
        for action in actions:
            if '*' in action:
                prefix = action.replace('*', '')
                expanded.extend([a for a in all_available_actions if a.startswith(prefix)])
            else:
                expanded.append(action)
        return list(set(expanded))
