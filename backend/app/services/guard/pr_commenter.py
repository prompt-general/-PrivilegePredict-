import requests
import os
from typing import Dict, Any
from ..models.guard import GuardDecision

class PRCommenter:
    """Utility to post analysis results as comments on GitHub pull requests"""

    @staticmethod
    def post_github_comment(repo: str, pr_number: int, decision: GuardDecision):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN not set, skipping PR comment.")
            return

        url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        status_emoji = "❌" if decision.status == "blocked" else ("⚠️" if decision.status == "warning" else "✅")
        
        body = f"## {status_emoji} PrivilegePredict IAM Analysis\n\n"
        body += f"**Status:** {decision.status.upper()}\n"
        body += f"**Risk Score:** {decision.risk_score}/100\n"
        body += f"**New Escalation Path:** {'Yes' if decision.new_escalation_path else 'No'}\n\n"
        
        if decision.reasons:
            body += "### Reasons for evaluation:\n"
            for reason in decision.reasons:
                body += f"- {reason}\n"
        
        body += f"\n---\n*Evaluation ID: {decision.evaluation_id}*"

        try:
            response = requests.post(url, json={"body": body}, headers=headers)
            response.raise_for_status()
            print(f"Successfully posted comment to PR #{pr_number}")
        except Exception as e:
            print(f"Failed to post GitHub comment: {e}")
