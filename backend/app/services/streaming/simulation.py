import time
import json
from .processor import StreamingEventProcessor
from .alerts import AlertService

class SimulatedStreamingListener:
    """Simulates listening to an event stream (AWS EventBridge / Azure Event Hub)"""

    def __init__(self):
        self.processor = StreamingEventProcessor()

    def run_simulation(self):
        print("Starting Simulated Streaming Support...")
        
        # Simulated stream of events
        mock_events = [
            {
                "id": "evt-001",
                "detail-type": "CreateRole",
                "detail": {
                    "userIdentity": {"arn": "aws::123456789012::user::admin-user"},
                    "requestParameters": {"roleName": "NewEvilRole"}
                }
            },
            {
                "id": "evt-002",
                "detail-type": "AttachRolePolicy",
                "detail": {
                    "userIdentity": {"arn": "aws::123456789012::user::admin-user"},
                    "requestParameters": {"roleName": "NewEvilRole", "policyArn": "arn:aws:iam::aws:policy/AdministratorAccess"}
                }
            }
        ]

        for raw_event in mock_events:
            print(f"Processing event {raw_event['id']}...")
            result = self.processor.process_event(raw_event)
            
            if result and result["is_high_risk"]:
                AlertService.send_alert(result)
            
            time.sleep(1)

if __name__ == "__main__":
    listener = SimulatedStreamingListener()
    listener.run_simulation()
