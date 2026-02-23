from typing import List, Optional, Dict
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

def get_full_graph() -> Dict:
    """Get all nodes and relationships for the full graph"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        # Get nodes
        nodes_result = session.run("MATCH (n:Identity) RETURN n")
        nodes = []
        for record in nodes_result:
            node = record['n']
            nodes.append({
                "id": node['id'],
                "name": node['name'],
                "type": node.get('type', 'unknown'),
                "provider": node.get('provider', 'unknown')
            })
        
        # Get policies too
        policy_result = session.run("MATCH (p:Policy) RETURN p")
        for record in policy_result:
            node = record['p']
            nodes.append({
                "id": node['id'],
                "name": node['name'],
                "type": "policy",
                "provider": node.get('provider', 'unknown')
            })

        # Get relationships
        rel_result = session.run("MATCH (a)-[r]->(b) RETURN a.id as source, b.id as target, type(r) as type")
        edges = []
        for record in rel_result:
            edges.append({
                "source": record['source'],
                "target": record['target'],
                "type": record['type']
            })
            
        return {"nodes": nodes, "edges": edges}