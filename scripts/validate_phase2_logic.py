import json
from datetime import datetime
from app.models.event import CloudEvent
from app.services.permissions.analyzer import EffectivePermissionAnalyzer
from app.models.identity import Identity

def mock_validation():
    print("Running Mock Validation for Effective Permission Engine...")
    
    # Mock Identity (Alice)
    # Alice has 's3:Get*' and 's3:List*' granted via a mock policy
    alice_id = "aws::123456789012::user::Alice"
    
    # Mock some Observed Events
    observed_actions = ["s3:GetObject", "s3:ListBucket"]
    
    # We need to ensure Neo4j has a mock policy for Alice for this to work in a real test
    # But for this script, we can test the analyzer logic if we mock the _get_granted_actions
    
    analyzer = EffectivePermissionAnalyzer()
    
    # Monkeypatch for testing
    analyzer._get_granted_actions = lambda x: ["s3:GetObject", "s3:PutObject", "s3:ListBucket", "s3:DeleteObject"]
    
    summary = analyzer.analyze_identity(alice_id, observed_actions)
    
    print(f"Analysis for {alice_id}:")
    print(f"  Granted: {summary.granted_count} actions")
    print(f"  Used: {summary.used_actions}")
    print(f"  Unused: {summary.unused_actions}")
    print(f"  Efficiency: {(summary.used_count/summary.granted_count)*100}%")
    
    assert summary.granted_count == 4
    assert summary.used_count == 2
    assert "s3:PutObject" in summary.unused_actions
    assert "s3:DeleteObject" in summary.unused_actions
    
    print("Validation Successful: Engine correctly identifies unused permissions.")

if __name__ == "__main__":
    mock_validation()
