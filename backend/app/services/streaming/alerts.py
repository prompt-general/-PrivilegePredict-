from typing import Dict, Any
import requests
import os

class AlertService:
    """Handles notification of high-risk events via Webhooks or internal state"""

    @staticmethod
    def send_alert(alert_data: Dict[str, Any]):
        message = alert_data.get("alert_message", "High-risk event detected")
        event = alert_data.get("event")
        
        print(f"🚨 ALERT: {message}")
        print(f"   Identity: {event.identity_id}")
        print(f"   Action: {event.action}")

        # Integration point for Slack/Webhooks
        webhook_url = os.getenv("ALERT_WEBHOOK_URL")
        if webhook_url:
            try:
                requests.post(webhook_url, json={
                    "text": message,
                    "identity": event.identity_id,
                    "action": event.action,
                    "provider": event.provider,
                    "timestamp": event.timestamp.isoformat()
                })
            except Exception as e:
                print(f"Failed to send webhook: {e}")

    @staticmethod
    def store_alert_in_db(alert_data: Dict[str, Any]):
        """Persist alert for dashboard display"""
        from ...graph.database import get_db_connection
        db = get_db_connection()
        driver = db.get_driver()
        
        event = alert_data.get("event")
        with driver.session() as session:
            session.run("""
                MATCH (i:Identity {id: $identity_id})
                CREATE (a:Alert {
                    id: $id,
                    message: $message,
                    action: $action,
                    timestamp: $timestamp,
                    risk_score: $score
                })
                CREATE (i)-[:TRIGGERED]->(a)
            """, 
            identity_id=event.identity_id,
            id=event.event_id,
            message=alert_data.get("alert_message"),
            action=event.action,
            timestamp=event.timestamp.isoformat(),
            score=alert_data.get("risk_score")
            )

