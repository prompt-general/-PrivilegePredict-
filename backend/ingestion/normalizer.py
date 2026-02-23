from typing import Dict, List, Any
import json

class IdentityNormalizer:
    """Normalize cloud provider identities into a unified graph model"""

    @staticmethod
    def normalize_aws_data(aws_data: Dict[str, Any], account_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Normalize AWS IAM data into unified identity model
        """
        normalized_data = {
            'identities': [],
            'policies': [],
            'relationships': []
        }

        # Normalize users
        for user in aws_data.get('users', []):
            user_id = f"aws::{account_id}::user::{user['user_name']}"
            identity = {
                'id': user_id,
                'provider': 'aws',
                'type': 'user',
                'name': user['user_name'],
                'account_id': account_id,
                'arn': user['arn']
            }
            normalized_data['identities'].append(identity)

            # Add relationship to groups
            for group_name in user.get('groups', []):
                normalized_data['relationships'].append({
                    'source': user_id,
                    'target': f"aws::{account_id}::group::{group_name}",
                    'type': 'MEMBER_OF'
                })

            # Add policy attachments
            for policy in user.get('attached_policies', []):
                normalized_data['relationships'].append({
                    'source': user_id,
                    'target': f"aws::{account_id}::policy::{policy['policy_name']}",
                    'type': 'ATTACHED_POLICY'
                })

        # Normalize groups
        for group in aws_data.get('groups', []):
            group_id = f"aws::{account_id}::group::{group['group_name']}"
            identity = {
                'id': group_id,
                'provider': 'aws',
                'type': 'group',
                'name': group['group_name'],
                'account_id': account_id,
                'arn': group['arn']
            }
            normalized_data['identities'].append(identity)

            # Add policy attachments
            for policy in group.get('attached_policies', []):
                normalized_data['relationships'].append({
                    'source': group_id,
                    'target': f"aws::{account_id}::policy::{policy['policy_name']}",
                    'type': 'ATTACHED_POLICY'
                })

        # Normalize roles
        for role in aws_data.get('roles', []):
            role_id = f"aws::{account_id}::role::{role['role_name']}"
            identity = {
                'id': role_id,
                'provider': 'aws',
                'type': 'role',
                'name': role['role_name'],
                'account_id': account_id,
                'arn': role['arn']
            }
            normalized_data['identities'].append(identity)

            # Add policy attachments
            for policy in role.get('attached_policies', []):
                normalized_data['relationships'].append({
                    'source': role_id,
                    'target': f"aws::{account_id}::policy::{policy['policy_name']}",
                    'type': 'ATTACHED_POLICY'
                })

            # Parse AssumeRole trust policy
            trust_policy = role.get('assume_role_policy', {})
            if isinstance(trust_policy, str):
                try:
                    trust_policy = json.loads(trust_policy)
                except:
                    trust_policy = {}
            
            statements = trust_policy.get('Statement', [])
            if isinstance(statements, dict): statements = [statements]
            
            for statement in statements:
                if statement.get('Effect') == 'Allow' and 'sts:AssumeRole' in str(statement.get('Action', '')):
                    principals = statement.get('Principal', {})
                    # Handle AWS principals (could be ARN of user, group, role)
                    aws_principals = principals.get('AWS', [])
                    if isinstance(aws_principals, str): aws_principals = [aws_principals]
                    
                    for p in aws_principals:
                        # Add TRUSTS relationship
                        # Note: p could be an ARN like arn:aws:iam::123456789012:user/alice
                        # We should ideally map this to our internal ID format if it belongs to this account
                        normalized_data['relationships'].append({
                            'source': role_id,
                            'target': p, # Using ARN directly for external or cross-account principals
                            'type': 'TRUSTS'
                        })

        # Normalize policies
        for policy in aws_data.get('policies', []):
            policy_obj = {
                'id': f"aws::{account_id}::policy::{policy['policy_name']}",
                'provider': 'aws',
                'name': policy['policy_name'],
                'arn': policy['arn'],
                'is_managed': True,
                'account_id': account_id
            }
            normalized_data['policies'].append(policy_obj)

        return normalized_data

    @staticmethod
    def normalize_azure_data(azure_data: Dict[str, Any], tenant_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Normalize Azure Entra ID data into unified identity model
        """
        normalized_data = {
            'identities': [],
            'policies': [],
            'relationships': []
        }

        # Normalize users
        for user in azure_data.get('users', []):
            user_id = f"azure::{tenant_id}::user::{user['id']}"
            identity = {
                'id': user_id,
                'provider': 'azure',
                'type': 'user',
                'name': user['name'],
                'account_id': tenant_id
            }
            normalized_data['identities'].append(identity)

        # Normalize groups
        for group in azure_data.get('groups', []):
            group_id = f"azure::{tenant_id}::group::{group['id']}"
            identity = {
                'id': group_id,
                'provider': 'azure',
                'type': 'group',
                'name': group['name'],
                'account_id': tenant_id
            }
            normalized_data['identities'].append(identity)

            # Add group memberships
            for member_id in group.get('members', []):
                # We don't know if the member is a user, group or SP yet
                # In Neo4j we'll search by ID
                normalized_data['relationships'].append({
                    'source': f"azure::{tenant_id}::entity::{member_id}", # Generic prefix to be resolved
                    'target': group_id,
                    'type': 'MEMBER_OF'
                })

        # Normalize service principals
        for sp in azure_data.get('service_principals', []):
            sp_id = f"azure::{tenant_id}::service_principal::{sp['id']}"
            identity = {
                'id': sp_id,
                'provider': 'azure',
                'type': 'service_principal',
                'name': sp['name'],
                'account_id': tenant_id
            }
            normalized_data['identities'].append(identity)

        # Add relationships from role assignments
        for assignment in azure_data.get('role_assignments', []):
            normalized_data['relationships'].append({
                'source': f"azure::{tenant_id}::entity::{assignment['principal_id']}",
                'target': f"azure::{tenant_id}::role::{assignment['role_definition_id']}",
                'type': 'HAS_ROLE'
            })

        return normalized_data

    @staticmethod
    def create_unified_identity_graph(aws_data: Dict[str, Any], azure_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Create a unified identity graph from normalized AWS and Azure data

        :param aws_data: Normalized AWS data
        :param azure_data: Normalized Azure data
        :return: Unified identity graph
        """
        unified_graph = {
            'identities': [],
            'policies': [],
            'relationships': []
        }

        # Combine identities
        unified_graph['identities'].extend(aws_data.get('identities', []))
        unified_graph['identities'].extend(azure_data.get('identities', []))

        # Combine policies
        unified_graph['policies'].extend(aws_data.get('policies', []))
        # Azure policies are role assignments, so they would be handled differently

        # Combine relationships
        unified_graph['relationships'].extend(aws_data.get('relationships', []))
        unified_graph['relationships'].extend(azure_data.get('relationships', []))

        return unified_graph