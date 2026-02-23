from typing import List, Optional
from ..models.identity import Identity
from ..graph.database import get_db_connection

def get_all_identities() -> List[Identity]:
    """Get all identities from the graph database"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        result = session.run("MATCH (i:Identity) RETURN i")
        identities = []
        for record in result:
            node = record['i']
            identities.append(Identity(
                id=node['id'],
                provider=node['provider'],
                type=node['type'],
                name=node['name'],
                account_id=node.get('account_id')
            ))
        return identities

def get_identity_by_id(identity_id: str) -> Optional[Identity]:
    """Get an identity by ID from the graph database"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        result = session.run("MATCH (i:Identity {id: $identity_id}) RETURN i", identity_id=identity_id)
        record = result.single()
        if record:
            node = record['i']
            return Identity(
                id=node['id'],
                provider=node['provider'],
                type=node['type'],
                name=node['name'],
                account_id=node.get('account_id')
            )
        return None