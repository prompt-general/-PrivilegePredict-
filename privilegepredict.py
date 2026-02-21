#!/usr/bin/env python3
"""
PrivilegePredict CLI Tool
"""

import argparse
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    parser = argparse.ArgumentParser(description='PrivilegePredict CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest cloud IAM data')
    ingest_parser.add_argument('--aws-access-key-id', help='AWS Access Key ID')
    ingest_parser.add_argument('--aws-secret-access-key', help='AWS Secret Access Key')
    ingest_parser.add_argument('--aws-region', default='us-east-1', help='AWS Region')
    ingest_parser.add_argument('--aws-account-id', help='AWS Account ID')
    ingest_parser.add_argument('--azure-tenant-id', help='Azure Tenant ID')
    ingest_parser.add_argument('--azure-client-id', help='Azure Client ID')
    ingest_parser.add_argument('--azure-client-secret', help='Azure Client Secret')
    ingest_parser.add_argument('--output', help='Output file prefix for JSON export')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query the identity graph')
    query_parser.add_argument('query_type', choices=['identities', 'paths', 'risk'], help='Type of query')
    query_parser.add_argument('--source', help='Source identity ID for path queries')
    query_parser.add_argument('--target', help='Target identity ID for path queries')

    # Visualization command
    viz_parser = subparsers.add_parser('viz', help='Start the visualization server')

    args = parser.parse_args()

    if args.command == 'ingest':
        # Import and run the ingestion module
        from backend.ingestion.main import main as ingest_main
        # We need to convert our args to the format expected by ingest_main
        print("Starting data ingestion...")
        # In a real implementation, we would call ingest_main with appropriate arguments

    elif args.command == 'query':
        print(f"Executing {args.query_type} query...")
        # In a real implementation, we would query the database

    elif args.command == 'viz':
        print("Starting visualization server...")
        # In a real implementation, we would start the web server

    else:
        parser.print_help()

if __name__ == '__main__':
    main()