import uuid
from typing import List
from ...models.guard import ProposedChange, GuardDecision
from .risk_engine import RiskScoringEngine
from .graph_simulator import GraphSimulator
from .feature_extractor import FeatureExtractor
from .audit_service import AuditService

class DecisionEngine:
    """Consolidates simulation and scoring to make a final block/allow decision"""

    def __init__(self):
        self.risk_engine = RiskScoringEngine()
        self.simulator = GraphSimulator()

    def evaluate(self, changes: List[ProposedChange], tenant_id: str = "default", block_threshold: float = 80.0, warning_threshold: float = 50.0) -> GuardDecision:
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
        eval_id = str(uuid.uuid4())

        for change in changes:
            introduces_escalation = self.simulator.simulate_change(change)
            score = self.risk_engine.compute_score(change, introduces_escalation)
            reasons = self.risk_engine.get_reasons(change, introduces_escalation)
            
            # Phase 3.5: Extract features for ML training
            features = FeatureExtractor.extract_features(change, introduces_escalation, score)
            
            if score > max_score:
                max_score = score
            
            if introduces_escalation:
                any_escalation = True
            
            all_reasons.extend(reasons)

        # Apply Thresholds
        status = "approved"
        if max_score >= block_threshold or any_escalation:
            status = "blocked"
        elif max_score >= warning_threshold:
            status = "warning"

        decision = GuardDecision(
            status=status,
            risk_score=max_score,
            reasons=list(set(all_reasons)),
            new_escalation_path=any_escalation,
            evaluation_id=eval_id
        )

        # Audit & Feature Archival
        for change in changes:
             # In a real environment, we'd batch this or log the highest risk change
             AuditService.log_evaluation(tenant_id, change, decision, features)

        return decision

