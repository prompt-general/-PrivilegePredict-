import json
import argparse
import requests
import os
import sys

# Add backend to path to import PRCommenter
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.services.guard.pr_commenter import PRCommenter
from app.models.guard import GuardDecision

def main():
    parser = argparse.ArgumentParser(description='PrivilegePredict CI Guard CLI')
    parser.add_argument('--plan', required=True, help='Path to terraform plan.json')
    parser.add_argument('--api-url', default='http://localhost:8000', help='PrivilegePredict API URL')
    parser.add_argument('--tenant', default='default', help='Tenant ID')
    parser.add_argument('--fail-on-warning', action='store_true', help='Treat warnings as blocks')
    parser.add_argument('--gh-repo', help='GitHub repository (e.g. org/repo)')
    parser.add_argument('--pr-number', type=int, help='Pull Request number')

    args = parser.parse_args()

    try:
        with open(args.plan, 'r') as f:
            plan_data = json.load(f)
    except Exception as e:
        print(f"Error reading plan file: {e}")
        sys.exit(1)

    print(f"Evaluating IAM changes for tenant: {args.tenant}...")
    
    try:
        response = requests.post(
            f"{args.api_url}/guard/evaluate",
            json={
                "tenant_id": args.tenant,
                "plan_json": plan_data
            }
        )
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(f"Error calling API: {e}")
        sys.exit(1)

    status = result["status"]
    score = result["risk_score"]
    reasons = result["reasons"]

    print("-" * 40)
    print(f"RESULT: {status.upper()}")
    print(f"RISK SCORE: {score}/100")
    print("-" * 40)

    if reasons:
        print("Reasons:")
        for r in reasons:
            print(f"- {r}")
    
    if result["new_escalation_path"]:
        print("\nALERT: This change introduces a NEW privilege escalation path!")

    # Post GitHub Comment if requested
    if args.gh_repo and args.pr_number:
        print(f"Posting comment to {args.gh_repo} PR #{args.pr_number}...")
        decision = GuardDecision(**result)
        PRCommenter.post_github_comment(args.gh_repo, args.pr_number, decision)

    if status == "blocked":
        print("\nPolicy violation: Change BLOCKED by CI Guard.")
        sys.exit(1)
    elif status == "warning" and args.fail_on_warning:
        print("\nPolicy violation: Change triggered WARNING (failing due to --fail-on-warning).")
        sys.exit(1)
    
    print("\nIdentity security checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
