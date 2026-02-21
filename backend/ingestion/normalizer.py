from typing import Dict, List, Any
import json

class IdentityNormalizer:
    """Normalize cloud provider identities into a unified graph model"""

    @staticmethod
    def normalize_aws_data(aws_data: Dict[str, Any], account_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Normalize AWS IAM data into unified identity model

        :param aws_data: Raw AWS IAM data
        :param account_id: AWS account ID
        :return: Normalized identity data
        """
        normalized_data = {
            'identities': [],
            'policies': [],
            'relationships': []
        }

        # Normalize users
        for user in aws_data.get('users', []):
            identity = {
                'id': f"aws::{account_id}::user::{user['user_name']}",
                'provider': 'aws',
                'type': 'user',
                'name': user['user_name'],
                'account_id': account_id,
                'arn': user['arn'],
                'create_date': user['create_date'].isoformat() if hasattr(user['create_date'], 'isoformat') else user['create_date']
            }
            normalized_data['identities'].append(identity)

            # Add relationship to groups (would need to fetch group memberships separately)
            # This is a simplified example

        # Normalize groups
        for group in aws_data.get('groups', []):
            identity = {
                'id': f"aws::{account_id}::group::{group['group_name']}",
                'provider': 'aws',
                'type': 'group',
                'name': group['group_name'],
                'account_id': account_id,
                'arn': group['arn'],
                'create_date': group['create_date'].isoformat() if hasattr(group['create_date'], 'isoformat') else group['create_date']
            }
            normalized_data['identities'].append(identity)

        # Normalize roles
        for role in aws_data.get('roles', []):
            identity = {
                'id': f"aws::{account_id}::role::{role['role_name']}",
                'provider': 'aws',
                'type': 'role',
                'name': role['role_name'],
                'account_id': account_id,
                'arn': role['arn'],
                'create_date': role['create_date'].isoformat() if hasattr(role['create_date'], 'isoformat') else role['create_date'],
                'assume_role_policy': json.dumps(role['assume_role_policy']) if isinstance(role['assume_role_policy'], dict) else role['assume_role_policy']
            }
            normalized_data['identities'].append(identity)

        # Normalize policies
        for policy in aws_data.get('policies', []):
            policy_obj = {
                'id': f"aws::{account_id}::policy::{policy['policy_name']}",
                'provider': 'aws',
                'name': policy['policy_name'],
                'arn': policy['arn'],
                'is_managed': True,  # AWS managed policies are managed by AWS
                'account_id': account_id,
                'attachment_count': policy['attachment_count']
            }
            normalized_data['policies'].append(policy_obj)

            # Get policy document
            try:
                policy_version = aws_data.get('iam_client').get_policy_version(
                    PolicyArn=policy['arn'],
                    VersionId=policy['default_version_id']
                )
                policy_obj['document'] = policy_version['PolicyVersion']['Document']
            except:
                pass

        # Add relationships (simplified)
        # In a real implementation, you would need to fetch:
        # - Group memberships (users in groups)
        # - Policy attachments (policies attached to users, groups, roles)
        # - Assume role relationships (trust policies)

        return normalized_data

    @staticmethod
    def normalize_azure_data(azure_data: Dict[str, Any], tenant_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Normalize Azure Entra ID data into unified identity model

        :param azure_data: Raw Azure Entra ID data
        :param tenant_id: Azure tenant ID
        :return: Normalized identity data
        """
        normalized_data = {
            'identities': [],
            'policies': [],  # Azure uses role assignments instead of policies
            'relationships': []
        }

        # Normalize users
        for user in azure_data.get('users', []):
            identity = {
                'id': f"azure::{tenant_id}::user::{user['id']}",
                'provider': 'azure',
                'type': 'user',
                'name': user['display_name'],
                'account_id': tenant_id,
                'user_principal_name': user['user_principal_name'],
                'mail': user['mail'],
                'account_enabled': user['account_enabled'],
                'job_title': user['job_title'],
                'department': user['department'],
                'created_datetime': user['created_datetime'].isoformat() if hasattr(user['created_datetime'], 'isoformat') else user['created_datetime']
            }
            normalized_data['identities'].append(identity)

        # Normalize groups
        for group in azure_data.get('groups', []):
            identity = {
                'id': f"azure::{tenant_id}::group::{group['id']}",
                'provider': 'azure',
                'type': 'group',
                'name': group['display_name'],
                'account_id': tenant_id,
                'description': group['description'],
                'mail': group['mail'],
                'mail_enabled': group['mail_enabled'],
                'security_enabled': group['security_enabled'],
                'created_datetime': group['created_datetime'].isoformat() if hasattr(group['created_datetime'], 'isoformat') else group['created_datetime']
            }
            normalized_data['identities'].append(identity)

        # Normalize service principals
        for sp in azure_data.get('service_principals', []):
            identity = {
                'id': f"azure::{tenant_id}::service_principal::{sp['id']}",
                'provider': 'azure',
                'type': 'service_principal',
                'name': sp['display_name'],
                'account_id': tenant_id,
                'app_id': sp['app_id'],
                'app_owner_organization_id': sp['app_owner_organization_id'],
                'account_enabled': sp['account_enabled'],
                'sign_in_audience': sp['sign_in_audience']
            }
            normalized_data['identities'].append(identity)

        # Add relationships from role assignments
        for assignment in azure_data.get('role_assignments', []):
            relationship = {
                'source': f"azure::{tenant_id}::entity::{assignment['principal_id']}",  # Simplified
                'target': f"azure::{tenant_id}::role::{assignment['role_definition_id']}",
                'type': 'HAS_ROLE',
                'scope': assignment['directory_scope_id'],
                'assignment_id': assignment['id']
            }
            normalized_data['relationships'].append(relationship)

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