from sqlalchemy import Column, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class EvaluationAudit(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String, index=True)
    identity_id = Column(String, index=True)
    risk_score = Column(Float)
    decision = Column(String)
    new_escalation = Column(Boolean)
    reasons = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
