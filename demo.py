#!/usr/bin/env python3
"""
PrivilegePredict Demo - Simplified version to demonstrate core concepts
"""

import json
from typing import Dict, List, Any

class IdentityGraphDemo:
    """Simplified demo of the PrivilegePredict identity graph functionality"""

    def __init__(self):
        self.identities = {}
        self.relationships = []

    def add_identity(self, identity_id: str, provider: str, type: str, name: str, **kwargs):
        """Add an identity to the graph"""
        self.identities[identity_id] = {
            "id": identity_id,
            "provider": provider,
            "type": type,
            "name": name,
            **kwargs
        }

    def add_relationship(self, source_id: str, target_id: str, relationship_type: str):
        """Add a relationship between two identities"""
        self.relationships.append({
            "source": source_id,
            "target": target_id,
            "type": relationship_type
        })

    def find_escalation_paths(self, source_id: str, target_id: str = None) -> List[Dict]:
        """Find escalation paths between identities (simplified)"""
        # This is a simplified version - in a real implementation,
        # this would use graph traversal algorithms

        paths = []

        # For demo purposes, let's just show direct relationships
        for rel in self.relationships:
            if rel["source"] == source_id:
                target_identity = self.identities.get(rel["target"], {})
                paths.append({
                    "nodes": [
                        self.identities[source_id],
                        target_identity
                    ],
                    "relationship": rel["type"]
                })

        return paths

    def get_high_risk_identities(self) -> List[Dict]:
        """Get identities that are considered high risk"""
        # In a real implementation, this would use risk scoring algorithms
        high_risk = []

        # For demo, let's consider roles with "admin" in the name as high risk
        for identity_id, identity in self.identities.items():
            if identity["type"] == "role" and "admin" in identity["name"].lower():
                identity["risk_score"] = 0.9
                high_risk.append(identity)

        return high_risk

def demo():
    """Run a demonstration of the PrivilegePredict functionality"""
    print("PrivilegePredict Demo")
    print("====================")

    # Create a demo graph
    graph = IdentityGraphDemo()

    # Add some sample AWS identities
    graph.add_identity(
        "aws::123456789012::user::alice",
        "aws",
        "user",
        "alice",
        account_id="123456789012"
    )

    graph.add_identity(
        "aws::123456789012::role::admin-role",
        "aws",
        "role",
        "admin-role",
        account_id="123456789012"
    )

    graph.add_identity(
        "aws::123456789012::group::developers",
        "aws",
        "group",
        "developers",
        account_id="123456789012"
    )

    # Add some sample Azure identities
    graph.add_identity(
        "azure::abcd1234-efgh-5678::user::bob",
        "azure",
        "user",
        "bob",
        account_id="abcd1234-efgh-5678"
    )

    graph.add_identity(
        "azure::abcd1234-efgh-5678::service_principal::app-sp",
        "azure",
        "service_principal",
        "app-sp",
        account_id="abcd1234-efgh-5678"
    )

    # Add relationships
    graph.add_relationship(
        "aws::123456789012::user::alice",
        "aws::123456789012::group::developers",
        "MEMBER_OF"
    )

    graph.add_relationship(
        "aws::123456789012::user::alice",
        "aws::123456789012::role::admin-role",
        "ASSUMES"
    )

    graph.add_relationship(
        "azure::abcd1234-efgh-5678::user::bob",
        "azure::abcd1234-efgh-5678::service_principal::app-sp",
        "CAN_ACCESS"
    )

    # Show all identities
    print("\nIdentities in the graph:")
    for identity_id, identity in graph.identities.items():
        print(f"  - {identity['name']} ({identity['type']}) [{identity['provider']}]")

    # Show relationships
    print("\nRelationships in the graph:")
    for rel in graph.relationships:
        source_name = graph.identities[rel["source"]]["name"]
        target_name = graph.identities[rel["target"]]["name"]
        print(f"  - {source_name} {rel['type']} {target_name}")

    # Find escalation paths
    print("\nEscalation paths from alice:")
    paths = graph.find_escalation_paths("aws::123456789012::user::alice")
    for path in paths:
        print(f"  - {path['nodes'][0]['name']} → {path['relationship']} → {path['nodes'][1]['name']}")

    # Show high-risk identities
    print("\nHigh-risk identities:")
    high_risk = graph.get_high_risk_identities()
    for identity in high_risk:
        print(f"  - {identity['name']} (risk score: {identity.get('risk_score', 'N/A')})")

if __name__ == "__main__":
    demo()