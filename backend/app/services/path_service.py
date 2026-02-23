from typing import List, Optional
from ..models.path import Path
from ..graph.database import get_db_connection

def find_escalation_paths(source_id: str, target_id: Optional[str] = None) -> List[Path]:
    """Find escalation paths between identities in the graph database"""
    db = get_db_connection()
    driver = db.get_driver()

    with driver.session() as session:
        if target_id:
            # Path to specific target
            query = """
            MATCH (a:Identity {id: $source_id}), (b:Identity {id: $target_id})
            MATCH p = shortestPath((a)-[*1..6]->(b))
            RETURN p
            """
            params = {"source_id": source_id, "target_id": target_id}
        else:
            # Path to any high-privilege node (e.g., admin roles)
            query = """
            MATCH (a:Identity {id: $source_id})
            MATCH (b:Identity)
            WHERE b.name CONTAINS 'admin' OR b.name CONTAINS 'Admin' OR b.high_privilege = true
            MATCH p = shortestPath((a)-[*1..6]->(b))
            RETURN p
            """
            params = {"source_id": source_id}

        result = session.run(query, **params)
        paths = []
        
        for record in result:
            neo4j_path = record['p']
            
            nodes = []
            for node in neo4j_path.nodes:
                nodes.append({
                    "id": node['id'],
                    "name": node['name'],
                    "type": node.get('type', 'unknown'),
                    "provider": node.get('provider', 'unknown')
                })
            
            relationships = []
            for rel in neo4j_path.relationships:
                relationships.append({
                    "source": rel.start_node['id'],
                    "target": rel.end_node['id'],
                    "type": rel.type,
                    "properties": dict(rel)
                })
            
            paths.append(Path(
                nodes=nodes,
                relationships=relationships,
                risk_score=0.9 if any('admin' in n['name'].lower() for n in nodes) else 0.5
            ))
            
        return paths