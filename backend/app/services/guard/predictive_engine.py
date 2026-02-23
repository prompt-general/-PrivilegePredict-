import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from typing import List, Dict, Any
import json

class PredictiveRiskModel:
    """Baseline implementation for predictive risk scoring (ML-ready)"""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        # In a real setup, we'd load a persisted model from model_registry.py
        self.is_trained = False

    def train_baseline(self, audit_logs: List[Dict[str, Any]]):
        """Trains a baseline model on archived evaluation features"""
        if not audit_logs:
            return

        # Prepare DataFrame from features
        data = []
        labels = []
        for log in audit_logs:
            features = log.get("features", {})
            if features:
                data.append(features)
                # Label: 1 if blocked, 0 otherwise
                labels.append(1 if log.get("decision") == "blocked" else 0)

        if not data:
            return

        df = pd.DataFrame(data)
        self.model.fit(df, labels)
        self.is_trained = True
        print(f"ML Baseline trained on {len(data)} evaluation samples.")

    def predict_risk(self, features: Dict[str, Any]) -> float:
        """Predicts risk probability using the ML model"""
        if not self.is_trained:
            # Fallback to rule engine score if model isn't trained
            return features.get("rule_engine_baseline", 0.0) / 100.0

        df = pd.DataFrame([features])
        # Returns probability of 'blocked' class
        prob = self.model.predict_proba(df)[0][1]
        return float(prob)
