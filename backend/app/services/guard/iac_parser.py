import json
from typing import List, Dict, Any
from ...models.guard import ProposedChange

class TerraformParser:
    """Parses Terraform plan -json output to extract IAM changes"""

    @staticmethod
    def parse_plan(plan_json: Dict[str, Any], account_id: str) -> List[ProposedChange]:
        changes = []
        resource_changes = plan_json.get("resource_changes", [])

        for rc in resource_changes:
            resource_type = rc.get("type", "")
            change = rc.get("change", {})
            actions = change.get("actions", [])
            
            # We focus on Create, Update, and Delete actions
            if "no-op" in actions or "read" in actions:
                continue

            after = change.get("after", {})
            before = change.get("before", {})

            if resource_type == "aws_iam_policy" or resource_type == "aws_iam_role_policy":
                # Handle inline or managed policy changes
                policy_doc = after.get("policy", {})
                if isinstance(policy_doc, str):
                    try:
                        policy_doc = json.loads(policy_doc)
                    except:
                        policy_doc = {}
                
                # identify the identity attached to this policy
                # For aws_iam_role_policy, it's 'role'
                # For aws_iam_user_policy, it's 'user'
                identity_name = after.get("role") or after.get("user") or after.get("group") or after.get("name")
                identity_type = "role" if after.get("role") else ("user" if after.get("user") else "policy")
                
                if identity_name:
                    from ..permissions.policy_parser import AWSPolicyParser
                    added_actions = AWSPolicyParser.get_actions_from_policy(policy_doc)
                    
                    changes.append(ProposedChange(
                        identity_id=f"aws::{account_id}::{identity_type}::{identity_name}",
                        identity_name=identity_name,
                        identity_type=identity_type,
                        added_permissions=added_actions,
                        provider="aws"
                    ))

            elif resource_type == "aws_iam_role_policy_attachment":
                role_name = after.get("role")
                policy_arn = after.get("policy_arn")
                if role_name and policy_arn:
                    # In a real scenario, we'd need to fetch the actions from the policy_arn
                    # For this MVP, we flag the attachment itself
                    changes.append(ProposedChange(
                        identity_id=f"aws::{account_id}::role::{role_name}",
                        identity_name=role_name,
                        identity_type="role",
                        added_permissions=["attach-policy:" + policy_arn],
                        provider="aws"
                    ))
                    
        return changes
