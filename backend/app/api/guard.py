from fastapi import APIRouter, HTTPException
from ..models.guard import CIRequest, GuardDecision
from ..services.guard.iac_parser import TerraformParser
from ..services.guard.decision_engine import DecisionEngine

router = APIRouter()

@router.post("/evaluate", response_model=GuardDecision)
async def evaluate_iac_changes(request: CIRequest):
    """
    Evaluate proposed IaC changes for identity security risks.
    Expected input: terraform plan -json or CloudFormation template.
    """
    try:
        # 1. Parse IaC (Currently supporting Terraform)
        # In a real scenario, we'd extract the account_id from the plan or request
        account_id = "123456789012" 
        parser = TerraformParser()
        proposed_changes = parser.parse_plan(request.plan_json, account_id)
        
        # 2. Evaluate
        engine = DecisionEngine()
        decision = engine.evaluate(
            proposed_changes, 
            tenant_id=request.tenant_id,
            block_threshold=request.block_threshold,
            warning_threshold=request.warning_threshold
        )
        
        # 3. Store in Audit Log (Future milestone)
        return decision

    except Exception as e:
        print(f"CI Evaluation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
