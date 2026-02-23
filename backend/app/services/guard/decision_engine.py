import uuid
from datetime import datetime
from typing import List
from ...models.guard import ProposedChange, GuardDecision
from .risk_engine import RiskScoringEngine
from .graph_simulator import GraphSimulator

class DecisionEngine:
    """Consolidates simulation and scoring to make a final block/allow decision"""

    def __init__(self):
        self.risk_engine = RiskScoringEngine()
        self.simulator = GraphSimulator()

    def evaluate(self, changes: List[ProposedChange]) -> GuardDecision:
        if not changes:
            return GuardDecision(
                status="approved",
                risk_score=0.0,
                reasons=["No IAM changes detected in the proposed plan."],
                new_escalation_path=False,
                evaluation_id=str(uuid.uuid4())
            )

        max_score = 0.0
        all_reasons = []
        any_escalation = False

        for change in changes:
            introduces_escalation = self.simulator.simulate_change(change)
            score = self.risk_engine.compute_score(change, introduces_escalation)
            reasons = self.risk_engine.get_reasons(change, introduces_escalation)
            
            if score > max_score:
                max_score = score
            
            if introduces_escalation:
                any_escalation = True
            
            all_reasons.extend(reasons)

        # Apply Thresholds
        status = "approved"
        if max_score >= 80 or any_escalation:
            status = "blocked"
        elif max_score >= 50:
            status = "warning"

        return GuardDecision(
            status=status,
            risk_score=max_score,
            reasons=list(set(all_reasons)), # deduplicate
            new_escalation_path=any_escalation,
            evaluation_id=str(uuid.uuid4())
        )
