#!/usr/bin/env python3
"""
Main ingestion script for PrivilegePredict
This script connects to cloud providers, retrieves IAM data, normalizes it, and stores it in the graph database.
"""

import argparse
import json
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ingestion.aws_connector import AWSConnector
from ingestion.azure_connector import AzureConnector
from ingestion.normalizer import IdentityNormalizer
from app.graph.database import get_db_connection

def ingest_aws_data(args):
    """Ingest AWS IAM data"""
    print("Connecting to AWS...")

    # Initialize AWS connector
    connector = AWSConnector(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name=args.aws_region
    )

    # Get all IAM data
    print(f"Retrieving IAM data for account {args.aws_account_id}...")
    aws_data = connector.get_all_iam_data(args.aws_account_id)

    # Normalize the data
    print("Normalizing AWS data...")
    normalized_aws_data = IdentityNormalizer.normalize_aws_data(aws_data, args.aws_account_id)

    # Save to file if requested
    if args.output:
        with open(f"{args.output}_aws.json", 'w') as f:
            json.dump(normalized_aws_data, f, indent=2, default=str)
        print(f"AWS data saved to {args.output}_aws.json")

    return normalized_aws_data

async def ingest_azure_data(args):
    """Ingest Azure Entra ID data"""
    print("Connecting to Azure...")

    # Initialize Azure connector
    connector = AzureConnector(
        tenant_id=args.azure_tenant_id,
        client_id=args.azure_client_id,
        client_secret=args.azure_client_secret
    )

    # Get all Entra ID data
    print(f"Retrieving Entra ID data for tenant {args.azure_tenant_id}...")
    azure_data = await connector.get_all_entra_id_data()

    # Normalize the data
    print("Normalizing Azure data...")
    normalized_azure_data = IdentityNormalizer.normalize_azure_data(azure_data, args.azure_tenant_id)

    # Save to file if requested
    if args.output:
        with open(f"{args.output}_azure.json", 'w') as f:
            json.dump(normalized_azure_data, f, indent=2, default=str)
        print(f"Azure data saved to {args.output}_azure.json")

    return normalized_azure_data

def store_in_graph_db(unified_graph):
    """Store the unified identity graph in Neo4j"""
    print("Storing data in Neo4j...")

    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        # Create constraints and indexes first
        print("Creating constraints and indexes...")
        session.run("""
            CREATE CONSTRAINT identity_id IF NOT EXISTS
            FOR (i:Identity) REQUIRE i.id IS UNIQUE
        """)

        session.run("""
            CREATE CONSTRAINT policy_id IF NOT EXISTS
            FOR (p:Policy) REQUIRE p.id IS UNIQUE
        """)

        session.run("""
            CREATE INDEX permission_action IF NOT EXISTS
            FOR (p:Permission) ON (p.action)
        """)

        # Insert identities
        print("Inserting identities...")
        for identity in unified_graph['identities']:
            session.run("""
                MERGE (i:Identity {id: $id})
                SET i.provider = $provider,
                    i.type = $type,
                    i.name = $name,
                    i.account_id = $account_id
            """, identity)

        # Insert policies
        print("Inserting policies...")
        for policy in unified_graph['policies']:
            session.run("""
                MERGE (p:Policy {id: $id})
                SET p.provider = $provider,
                    p.name = $name,
                    p.is_managed = $is_managed
            """, policy)

        # Insert relationships
        print("Inserting relationships...")
        for relationship in unified_graph['relationships']:
            session.run("""
                MATCH (a:Identity {id: $source})
                MATCH (b:Identity {id: $target})
                MERGE (a)-[r:RELATIONSHIP]->(b)
                SET r.type = $type
            """, relationship)

    print("Data stored successfully!")

def main():
    parser = argparse.ArgumentParser(description='PrivilegePredict Ingestion Tool')
    parser.add_argument('--output', help='Output file prefix for JSON export')

    # AWS arguments
    aws_group = parser.add_argument_group('AWS Options')
    aws_group.add_argument('--aws-access-key-id', help='AWS Access Key ID')
    aws_group.add_argument('--aws-secret-access-key', help='AWS Secret Access Key')
    aws_group.add_argument('--aws-region', default='us-east-1', help='AWS Region')
    aws_group.add_argument('--aws-account-id', help='AWS Account ID')

    # Azure arguments
    azure_group = parser.add_argument_group('Azure Options')
    azure_group.add_argument('--azure-tenant-id', help='Azure Tenant ID')
    azure_group.add_argument('--azure-client-id', help='Azure Client ID')
    azure_group.add_argument('--azure-client-secret', help='Azure Client Secret')

    args = parser.parse_args()

    # Check if we have any cloud provider credentials
    has_aws = args.aws_access_key_id and args.aws_secret_access_key and args.aws_account_id
    has_azure = args.azure_tenant_id and args.azure_client_id and args.azure_client_secret

    if not has_aws and not has_azure:
        print("Error: You must provide credentials for at least one cloud provider.")
        parser.print_help()
        return 1

    # Ingest data from cloud providers
    aws_data = None
    azure_data = None
    unified_graph = {'identities': [], 'policies': [], 'relationships': []}

    if has_aws:
        try:
            aws_data = ingest_aws_data(args)
            unified_graph['identities'].extend(aws_data.get('identities', []))
            unified_graph['policies'].extend(aws_data.get('policies', []))
            unified_graph['relationships'].extend(aws_data.get('relationships', []))
        except Exception as e:
            print(f"Error ingesting AWS data: {e}")
            return 1

    if has_azure:
        try:
            import asyncio
            azure_data = asyncio.run(ingest_azure_data(args))
            unified_graph['identities'].extend(azure_data.get('identities', []))
            # Azure policies are role assignments, handled differently
            unified_graph['relationships'].extend(azure_data.get('relationships', []))
        except Exception as e:
            print(f"Error ingesting Azure data: {e}")
            return 1

    # Store in graph database
    if aws_data or azure_data:
        try:
            store_in_graph_db(unified_graph)
        except Exception as e:
            print(f"Error storing data in graph database: {e}")
            return 1

    print("Ingestion completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())