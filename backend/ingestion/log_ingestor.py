import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from .aws_connector import AWSConnector
from ..app.models.event import CloudEvent

class AWSLogIngestor:
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None, region_name: str = "us-east-1"):
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.ct_client = self.session.client('cloudtrail')

    def fetch_historical_events(self, days: int = 90) -> List[CloudEvent]:
        """
        Fetch historical events from CloudTrail using LookupEvents.
        Note: This is limited to the last 90 days and has API rate limits.
        """
        events = []
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        paginator = self.ct_client.get_paginator('lookup_events')
        
        # We look for events related to IAM actions or resource access
        # In a real scenario, we'd filter for data plane + control plane events
        for page in paginator.paginate(StartTime=start_time, EndTime=end_time):
            for event in page['Events']:
                raw_data = json.loads(event['CloudTrailEvent'])
                
                # Extract identity ID from user identity
                user_identity = raw_data.get('userIdentity', {})
                identity_id = self._extract_identity_id(user_identity, raw_data.get('recipientAccountId'))
                
                if not identity_id:
                    continue

                events.append(CloudEvent(
                    event_id=event['EventId'],
                    timestamp=event['EventTime'],
                    provider="aws",
                    identity_id=identity_id,
                    action=event['EventName'],
                    service=event['EventSource'].split('.')[0], # e.g. s3.amazonaws.com -> s3
                    resource=self._extract_resource(raw_data),
                    source_ip=raw_data.get('sourceIPAddress'),
                    user_agent=raw_data.get('userAgent')
                ))
        
        return events

    def _extract_identity_id(self, user_identity: Dict, account_id: str) -> str:
        """Extract a unified ID compatible with our Phase 1 graph"""
        type = user_identity.get('type')
        if type == 'IAMUser':
            return f"aws::{account_id}::user::{user_identity.get('userName')}"
        elif type == 'AssumedRole':
            # arn:aws:sts::123456789012:assumed-role/RoleName/SessionName
            arn = user_identity.get('arn', '')
            if 'assumed-role/' in arn:
                role_name = arn.split('assumed-role/')[1].split('/')[0]
                return f"aws::{account_id}::role::{role_name}"
        return None

    def _extract_resource(self, raw_data: Dict) -> str:
        resources = raw_data.get('resources', [])
        if resources:
            return resources[0].get('ARN', resources[0].get('resourceName'))
        return None
