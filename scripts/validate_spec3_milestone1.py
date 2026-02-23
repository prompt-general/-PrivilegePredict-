import json
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.guard.iac_parser import TerraformParser
from app.services.guard.decision_engine import DecisionEngine

def validate_milestone1():
    print("Validating Spec 3 Milestone 1: Terraform Guard...")
    
    # 1. Load mock plan
    plan_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'mock_tf_plan_escalation.json')
    with open(plan_path, 'r') as f:
        plan_json = json.load(f)
    
    # 2. Parse
    parser = TerraformParser()
    changes = parser.parse_plan(plan_json, "123456789012")
    
    print(f"Extracted {len(changes)} changes.")
    for c in changes:
        print(f"  Target: {c.identity_id}")
        print(f"  Actions: {c.added_permissions}")
    
    # 3. Decision Engine
    engine = DecisionEngine()
    
    # Monkeypatch simulator for unit test (avoid Neo4j connection)
    engine.simulator.simulate_change = lambda x: True # Assume it finds an escalation for this test
    
    decision = engine.evaluate(changes)
    
    print("-" * 30)
    print(f"Decision: {decision.status}")
    print(f"Risk Score: {decision.risk_score}")
    print(f"Reasons: {decision.reasons}")
    
    assert decision.status == "blocked"
    assert decision.risk_score >= 80
    assert any("iam:PassRole" in r for r in decision.reasons)
    
    print("\nMilestone 1 Validation Successful: Terraform changes correctly blocked.")

if __name__ == "__main__":
    validate_milestone1()
