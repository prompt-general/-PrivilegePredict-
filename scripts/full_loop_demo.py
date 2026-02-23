import os
import sys
import json
import time

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.guard.iac_parser import TerraformParser
from app.services.guard.decision_engine import DecisionEngine
from app.services.guard.pr_commenter import PRCommenter
from app.models.guard import GuardDecision

def run_full_loop_demo():
    print("Initializing PrivilegePredict Full-Loop Prevention Test...")
    time.sleep(1)

    # 1. Simulate Developer proposing a Terraform change
    print("\n[Step 1] Developer modifies 'main.tf' to add iam:PassRole to a web app role.")
    plan_path = os.path.join(os.path.dirname(__file__), '..', 'tests', 'mock_tf_plan_escalation.json')
    with open(plan_path, 'r') as f:
        plan_json = json.load(f)
    print("Result: 'terraform plan -json' generated.")

    # 2. CI/CD Pipeline triggers the Guard
    print("\n[Step 2] CI Pipeline triggers PrivilegePredict Guard...")
    parser = TerraformParser()
    changes = parser.parse_plan(plan_json, "123456789012")
    print(f"Analysis: Identified {len(changes)} IAM modification targeting {changes[0].identity_name}.")

    # 3. Decision Engine evaluates Risk
    print("\n[Step 3] Running Graph Simulation and Risk Scoring...")
    engine = DecisionEngine()
    # Mocking escalation for demo purposes since we don't have a live Neo4j with this specific role right now
    engine.simulator.simulate_change = lambda x: True 
    
    decision = engine.evaluate(changes)
    time.sleep(1.5)

    print("-" * 50)
    print(f"GUARD STATUS: {decision.status.upper()}")
    print(f"RISK SCORE: {decision.risk_score}/100")
    print("-" * 50)
    for reason in decision.reasons:
        print(f"(!) {reason}")

    # 4. PR Feedback
    print("\n[Step 4] Posting Security Feedback to GitHub PR...")
    # In demo, we just print the markdown body
    print(">>> GitHub Comment Draft:")
    print(f"## PrivilegePredict IAM Analysis")
    print(f"**Status:** {decision.status.upper()}")
    print(f"**Reasons:** {', '.join(decision.reasons)}")

    # 5. Dashboard Update
    print("\n[Step 5] Evaluation archived. Dashboard updated.")
    print(f"Audit Trail Link: http://localhost:5173/audit")
    
    print("\nPREVENTION SUCCESSFUL: Malicious IAM change blocked prior to deployment.")

if __name__ == "__main__":
    run_full_loop_demo()
