from typing import Dict, Any, List
import json
from datetime import datetime
from ..models.event import CloudEvent
from ..services.permissions.analyzer import EffectivePermissionAnalyzer
from ..services.identity_service import get_identity_by_id

class StreamingEventProcessor:
    """Processes incoming IAM change events in near real-time"""

    def __init__(self):
        self.analyzer = EffectivePermissionAnalyzer()

    def process_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a raw event from EventBridge or Event Hub.
        Detects if the event is a high-risk IAM change.
        """
        # 1. Normalize Event
        event = self._normalize_event(raw_event)
        if not event:
            return None

        # 2. Risk Evaluation
        risk_details = self._evaluate_event_risk(event)
        
        # 3. Update Graph (Increment used permissions if it's a usage event)
        # Or trigger re-analysis if it's a structural IAM change
        if self._is_iam_change(event):
            # In a real scenario, we'd trigger a background re-analysis of the identity
            print(f"Detected IAM Change for {event.identity_id}: {event.action}")
            # Mark for re-analysis in Neo4j
            self._mark_identity_dirty(event.identity_id)

        return {
            "event": event,
            "risk_score": risk_details.get("score", 0),
            "is_high_risk": risk_details.get("is_high_risk", False),
            "alert_message": risk_details.get("message")
        }

    def _normalize_event(self, raw_event: Dict[str, Any]) -> CloudEvent:
        # Placeholder for provider-specific normalization logic
        # For now, simplistic AWS EventBridge mapping
        detail = raw_event.get('detail', {})
        return CloudEvent(
            event_id=raw_event.get('id', 'unknown'),
            timestamp=datetime.now(),
            provider="aws",
            identity_id=detail.get('userIdentity', {}).get('arn', 'unknown'),
            action=raw_event.get('detail-type', 'unknown'),
            service="iam",
            resource=detail.get('requestParameters', {}).get('roleName')
        )

    def _is_iam_change(self, event: CloudEvent) -> bool:
        iam_change_actions = [
            "CreateRole", "PutRolePolicy", "AttachRolePolicy",
            "CreateUser", "AttachUserPolicy", "AddUserToGroup",
            "UpdateAssumeRolePolicy"
        ]
        return any(action in event.action for action in iam_change_actions)

    def _evaluate_event_risk(self, event: CloudEvent) -> Dict[str, Any]:
        """Simple heuristic for real-time risk scoring"""
        high_risk_keywords = ["Admin", "FullAccess", "Star", "AssumeRole"]
        is_high_risk = any(kw in event.action for kw in high_risk_keywords)
        
        return {
            "score": 0.9 if is_high_risk else 0.1,
            "is_high_risk": is_high_risk,
            "message": f"High-risk IAM event detected: {event.action} on {event.resource}" if is_high_risk else None
        }

    def _mark_identity_dirty(self, identity_id: str):
        # Implementation to mark node in Neo4j for re-analysis
        pass
