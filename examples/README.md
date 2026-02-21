#!/usr/bin/env python3
"""
Example script demonstrating how to use the PrivilegePredict ingestion tool
"""

import json
import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    print("PrivilegePredict Example Usage")
    print("==============================")

    # This is a placeholder example script
    # In a real scenario, you would:
    # 1. Configure your cloud provider credentials
    # 2. Run the ingestion process
    # 3. Query the graph database

    example_config = {
        "aws": {
            "account_id": "123456789012",
            "region": "us-east-1"
        },
        "azure": {
            "tenant_id": "abcd1234-efgh-5678-ijkl-9012mnopqrst",
            "client_id": "your-client-id",
            "client_secret": "your-client-secret"
        },
        "neo4j": {
            "uri": "bolt://localhost:7687",
            "user": "neo4j",
            "password": "password"
        }
    }

    print("\nExample configuration:")
    print(json.dumps(example_config, indent=2))

    print("\nTo run the ingestion process:")
    print("python backend/ingestion/main.py \\")
    print("  --aws-access-key-id YOUR_AWS_ACCESS_KEY_ID \\")
    print("  --aws-secret-access-key YOUR_AWS_SECRET_ACCESS_KEY \\")
    print("  --aws-account-id 123456789012 \\")
    print("  --azure-tenant-id your-tenant-id \\")
    print("  --azure-client-id your-client-id \\")
    print("  --azure-client-secret your-client-secret")

    print("\nTo start the web interface:")
    print("docker-compose up")

if __name__ == "__main__":
    main()