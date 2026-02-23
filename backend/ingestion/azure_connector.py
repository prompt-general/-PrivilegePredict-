from typing import Dict, List, Any
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
from msgraph.generated.role_management.role_management_request_builder import RoleManagementRequestBuilder

class AzureConnector:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        Initialize Azure connector

        :param tenant_id: Azure AD tenant ID
        :param client_id: Application (client) ID
        :param client_secret: Client secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

        # Create credential object
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

        # Create Graph service client
        self.client = GraphServiceClient(self.credential, ['https://graph.microsoft.com/.default'])

    async def get_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        try:
            users = await self.client.users.get()
            user_list = []

            if users.value:
                for user in users.value:
                    user_list.append({
                        'id': user.id,
                        'display_name': user.display_name,
                        'user_principal_name': user.user_principal_name,
                        'mail': user.mail,
                        'account_enabled': user.account_enabled,
                        'job_title': user.job_title,
                        'department': user.department,
                        'created_datetime': user.created_datetime
                    })

            return user_list
        except Exception as e:
            print(f"Error getting users: {e}")
            return []

    async def get_groups(self) -> List[Dict[str, Any]]:
        """Get all groups"""
        try:
            groups = await self.client.groups.get()
            group_list = []

            if groups.value:
                for group in groups.value:
                    group_list.append({
                        'id': group.id,
                        'display_name': group.display_name,
                        'description': group.description,
                        'mail': group.mail,
                        'mail_enabled': group.mail_enabled,
                        'security_enabled': group.security_enabled,
                        'created_datetime': group.created_date_time
                    })

            return group_list
        except Exception as e:
            print(f"Error getting groups: {e}")
            return []

    async def get_service_principals(self) -> List[Dict[str, Any]]:
        """Get all service principals"""
        try:
            service_principals = await self.client.service_principals.get()
            sp_list = []

            if service_principals.value:
                for sp in service_principals.value:
                    sp_list.append({
                        'id': sp.id,
                        'display_name': sp.display_name,
                        'app_id': sp.app_id,
                        'app_owner_organization_id': sp.app_owner_organization_id,
                        'account_enabled': sp.account_enabled,
                        'sign_in_audience': sp.sign_in_audience,
                        'preferred_token_signing_key_thumbprint': sp.preferred_token_signing_key_thumbprint
                    })

            return sp_list
        except Exception as e:
            print(f"Error getting service principals: {e}")
            return []

    async def get_role_assignments(self) -> List[Dict[str, Any]]:
        """Get all role assignments"""
        try:
            # Get role assignments from role management
            role_assignments = await self.client.role_management.directory.role_assignments.get()
            assignment_list = []

            if role_assignments.value:
                for assignment in role_assignments.value:
                    assignment_list.append({
                        'id': assignment.id,
                        'principal_id': assignment.principal_id,
                        'role_definition_id': assignment.role_definition_id,
                        'directory_scope_id': assignment.directory_scope_id,
                        'app_scope_id': assignment.app_scope_id
                    })

            return assignment_list
        except Exception as e:
            print(f"Error getting role assignments: {e}")
            return []

    async def get_role_definitions(self) -> List[Dict[str, Any]]:
        """Get all role definitions"""
        try:
            # Get role definitions from role management
            role_definitions = await self.client.role_management.directory.role_definitions.get()
            definition_list = []

            if role_definitions.value:
                for definition in role_definitions.value:
                    definition_list.append({
                        'id': definition.id,
                        'display_name': definition.display_name,
                        'description': definition.description,
                        'is_builtin': definition.is_built_in,
                        'is_privileged': definition.is_privileged,
                        'template_id': definition.template_id
                    })

            return definition_list
        except Exception as e:
            print(f"Error getting role definitions: {e}")
            return []

    async def get_group_members(self, group_id: str) -> List[str]:
        """Get members of a group"""
        try:
            members = await self.client.groups.by_group_id(group_id).members.get()
            member_ids = []
            if members.value:
                for member in members.value:
                    member_ids.append(member.id)
            return member_ids
        except Exception as e:
            print(f"Error getting group members: {e}")
            return []

    async def get_all_entra_id_data(self) -> Dict[str, Any]:
        """
        Get all Entra ID (Azure AD) data
        """
        users = await self.get_users()
        groups = await self.get_groups()
        service_principals = await self.get_service_principals()
        role_assignments = await self.get_role_assignments()
        role_definitions = await self.get_role_definitions()

        # Get group members
        for group in groups:
            group['members'] = await self.get_group_members(group['id'])

        return {
            'tenant_id': self.tenant_id,
            'users': users,
            'groups': groups,
            'service_principals': service_principals,
            'role_assignments': role_assignments,
            'role_definitions': role_definitions
        }

# Example usage:
# import asyncio
#
# async def main():
#     connector = AzureConnector(
#         tenant_id="your-tenant-id",
#         client_id="your-client-id",
#         client_secret="your-client-secret"
#     )
#
#     entra_id_data = await connector.get_all_entra_id_data()
#     print(json.dumps(entra_id_data, indent=2, default=str))
#
# asyncio.run(main())