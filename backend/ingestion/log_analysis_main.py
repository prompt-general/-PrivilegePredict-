#!/usr/bin/env python3
import argparse
import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ingestion.log_ingestor import AWSLogIngestor
from app.services.permissions.analyzer import EffectivePermissionAnalyzer
from app.services.identity_service import get_all_identities

def main():
    parser = argparse.ArgumentParser(description='PrivilegePredict Log Analysis Tool (Phase 2)')
    parser.add_argument('--days', type=int, default=30, help='Number of days of history to analyze')
    parser.add_argument('--aws-access-key-id', help='AWS Access Key ID')
    parser.add_argument('--aws-secret-access-key', help='AWS Secret Access Key')
    parser.add_argument('--aws-region', default='us-east-1', help='AWS Region')
    
    args = parser.parse_args()

    print(f"Starting batch log analysis for the last {args.days} days...")

    # 1. Fetch Logs
    ingestor = AWSLogIngestor(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        region_name=args.aws_region
    )
    
    print("Fetching CloudTrail events...")
    try:
        events = ingestor.fetch_historical_events(days=args.days)
        print(f"Retrieved {len(events)} events.")
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return 1

    # Group events by identity
    identity_usage = {}
    for event in events:
        if event.identity_id not in identity_usage:
            identity_usage[event.identity_id] = set()
        identity_usage[event.identity_id].add(event.action)

    # 2. Analyze against Graph
    analyzer = EffectivePermissionAnalyzer()
    
    # Get all identities from graph to ensure we analyze even those with NO usage
    all_identities = get_all_identities()
    print(f"Analyzing {len(all_identities)} identities...")

    for identity in all_identities:
        observed_actions = list(identity_usage.get(identity.id, []))
        summary = analyzer.analyze_identity(identity.id, observed_actions)
        
        print(f"Identity: {identity.name}")
        print(f"  Granted: {summary.granted_count}, Used: {summary.used_count}")
        print(f"  Unused: {summary.over_permissive_count}")
        
        # 3. Update Graph
        analyzer.update_graph_with_usage(summary)

    print("Success: Effective permission analysis complete.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
