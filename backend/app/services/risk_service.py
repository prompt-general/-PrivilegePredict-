from typing import List, Dict, Any
from ..models.identity import Identity
from ..graph.database import get_db_connection

def get_high_risk_identities() -> List[Identity]:
    """Get all high-risk identities from the graph database"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        query = """
        MATCH (i:Identity)
        WHERE i.name CONTAINS 'admin' OR i.name CONTAINS 'Admin' OR i.high_privilege = true
        RETURN i
        """
        result = session.run(query)
        identities = []
        for record in result:
            node = record['i']
            identities.append(Identity(
                id=node['id'],
                provider=node['provider'],
                type=node['type'],
                name=node['name']
            ))
        return identities

def get_recent_alerts() -> List[Dict[str, Any]]:
    """Get most recent IAM alerts"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        query = """
        MATCH (i:Identity)-[:TRIGGERED]->(a:Alert)
        RETURN a, i.name as identity_name
        ORDER BY a.timestamp DESC
        LIMIT 10
        """
        result = session.run(query)
        alerts = []
        for record in result:
            alert = dict(record['a'])
            alert['identity_name'] = record['identity_name']
            alerts.append(alert)
        return alerts