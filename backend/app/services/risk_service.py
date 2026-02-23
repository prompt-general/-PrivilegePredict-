from typing import List
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