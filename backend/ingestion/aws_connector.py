import boto3
from typing import Dict, List, Any
import json

class AWSConnector:
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None, region_name: str = "us-east-1"):
        """
        Initialize AWS connector

        :param aws_access_key_id: AWS access key ID
        :param aws_secret_access_key: AWS secret access key
        :param region_name: AWS region name
        """
        if aws_access_key_id and aws_secret_access_key:
            self.session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )
        else:
            # Use default credentials (IAM role, ~/.aws/credentials, etc.)
            self.session = boto3.Session(region_name=region_name)

        self.iam_client = self.session.client('iam')

    def get_users(self) -> List[Dict[str, Any]]:
        """Get all IAM users"""
        users = []
        paginator = self.iam_client.get_paginator('list_users')

        for page in paginator.paginate():
            for user in page['Users']:
                users.append({
                    'arn': user['Arn'],
                    'create_date': user['CreateDate'],
                    'path': user['Path'],
                    'user_id': user['UserId'],
                    'user_name': user['UserName']
                })

        return users

    def get_groups(self) -> List[Dict[str, Any]]:
        """Get all IAM groups"""
        groups = []
        paginator = self.iam_client.get_paginator('list_groups')

        for page in paginator.paginate():
            for group in page['Groups']:
                groups.append({
                    'arn': group['Arn'],
                    'create_date': group['CreateDate'],
                    'path': group['Path'],
                    'group_id': group['GroupId'],
                    'group_name': group['GroupName']
                })

        return groups

    def get_roles(self) -> List[Dict[str, Any]]:
        """Get all IAM roles"""
        roles = []
        paginator = self.iam_client.get_paginator('list_roles')

        for page in paginator.paginate():
            for role in page['Roles']:
                roles.append({
                    'arn': role['Arn'],
                    'create_date': role['CreateDate'],
                    'path': role['Path'],
                    'role_id': role['RoleId'],
                    'role_name': role['RoleName'],
                    'assume_role_policy': role['AssumeRolePolicyDocument']
                })

        return roles

    def get_policies(self) -> List[Dict[str, Any]]:
        """Get all IAM policies"""
        policies = []
        paginator = self.iam_client.get_paginator('list_policies')

        for page in paginator.paginate(Scope='Local'):  # Local policies only
            for policy in page['Policies']:
                policies.append({
                    'arn': policy['Arn'],
                    'attachment_count': policy['AttachmentCount'],
                    'create_date': policy['CreateDate'],
                    'is_attachable': policy['IsAttachable'],
                    'path': policy['Path'],
                    'policy_id': policy['PolicyId'],
                    'policy_name': policy['PolicyName'],
                    'default_version_id': policy['DefaultVersionId']
                })

        return policies

    def get_policy_version(self, policy_arn: str, version_id: str) -> Dict[str, Any]:
        """Get a specific version of a policy"""
        response = self.iam_client.get_policy_version(
            PolicyArn=policy_arn,
            VersionId=version_id
        )
        return response['PolicyVersion']

    def get_attached_group_policies(self, group_name: str) -> List[Dict[str, Any]]:
        """Get policies attached to a group"""
        policies = []
        paginator = self.iam_client.get_paginator('list_attached_group_policies')

        for page in paginator.paginate(GroupName=group_name):
            for policy in page['AttachedPolicies']:
                policies.append({
                    'policy_arn': policy['PolicyArn'],
                    'policy_name': policy['PolicyName']
                })

        return policies

    def get_attached_role_policies(self, role_name: str) -> List[Dict[str, Any]]:
        """Get policies attached to a role"""
        policies = []
        paginator = self.iam_client.get_paginator('list_attached_role_policies')

        for page in paginator.paginate(RoleName=role_name):
            for policy in page['AttachedPolicies']:
                policies.append({
                    'policy_arn': policy['PolicyArn'],
                    'policy_name': policy['PolicyName']
                })

        return policies

    def get_attached_user_policies(self, user_name: str) -> List[Dict[str, Any]]:
        """Get policies attached to a user"""
        policies = []
        paginator = self.iam_client.get_paginator('list_attached_user_policies')

        for page in paginator.paginate(UserName=user_name):
            for policy in page['AttachedPolicies']:
                policies.append({
                    'policy_arn': policy['PolicyArn'],
                    'policy_name': policy['PolicyName']
                })

        return policies

    def get_group_users(self, group_name: str) -> List[str]:
        """Get users in a group"""
        users = []
        paginator = self.iam_client.get_paginator('get_group')
        for page in paginator.paginate(GroupName=group_name):
            for user in page['Users']:
                users.append(user['UserName'])
        return users

    def get_user_groups(self, user_name: str) -> List[str]:
        """Get groups for a user"""
        groups = []
        paginator = self.iam_client.get_paginator('list_groups_for_user')
        for page in paginator.paginate(UserName=user_name):
            for group in page['Groups']:
                groups.append(group['GroupName'])
        return groups

    def get_all_iam_data(self, account_id: str) -> Dict[str, Any]:
        """
        Get all IAM data for an account including relationships
        """
        users = self.get_users()
        groups = self.get_groups()
        roles = self.get_roles()
        policies = self.get_policies()

        # Get relationships
        for user in users:
            user['attached_policies'] = self.get_attached_user_policies(user['user_name'])
            user['groups'] = self.get_user_groups(user['user_name'])
        
        for group in groups:
            group['attached_policies'] = self.get_attached_group_policies(group['group_name'])
        
        for role in roles:
            role['attached_policies'] = self.get_attached_role_policies(role['role_name'])

        return {
            'account_id': account_id,
            'users': users,
            'groups': groups,
            'roles': roles,
            'policies': policies
        }

# Example usage:
# connector = AWSConnector()
# iam_data = connector.get_all_iam_data("123456789012")
# print(json.dumps(iam_data, indent=2, default=str))