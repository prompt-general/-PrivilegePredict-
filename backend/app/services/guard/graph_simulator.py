from typing import List, Dict, Any
from ...graph.database import get_db_connection
from ...models.guard import ProposedChange

class GraphSimulator:
    """Simulates IAM changes on the identity graph to detect new escalation paths"""

    def __init__(self):
        self.db = get_db_connection()

    def simulate_change(self, change: ProposedChange) -> bool:
        """
        Returns True if the change introduces a new path to a high-privilege node.
        """
        driver = self.db.get_driver()
        with driver.session() as session:
            # 1. Check if the identity already has an escalation path
            # We use the existing pathfinding logic
            existing_path = self._has_path_to_admin(session, change.identity_id)
            if existing_path:
                return False # Already has escalation, not "newly introduced" by this specific change

            # 2. Simulate the new permissions
            # If the new permission allows assuming a role or passing a role, 
            # we check if those targets can reach admin
            for action in change.added_permissions:
                if "AssumeRole" in action or "PassRole" in action:
                    # In a real scenario, we'd parse the 'Resource' field to find the target role
                    # For this simulation, we check if ANY role reachable by this action leads to admin
                    if self._check_potential_escalation(session, change.identity_id, action):
                        return True

            # 3. Check for direct Admin power
            if any(p == "*" or "AdministratorAccess" in p or "iam:*" in p for p in change.added_permissions):
                return True

        return False

    def _has_path_to_admin(self, session, identity_id: str) -> bool:
        query = """
        MATCH (a:Identity {id: $id}), (b:Identity)
        WHERE (b.name CONTAINS 'admin' OR b.name CONTAINS 'Admin' OR b.high_privilege = true)
        AND a.id <> b.id
        MATCH p = shortestPath((a)-[*1..6]->(b))
        RETURN count(p) > 0 as has_path
        """
        result = session.run(query, id=identity_id)
        record = result.single()
        return record["has_path"] if record else False

    def _check_potential_escalation(self, session, identity_id: str, action: str) -> bool:
        # Simplistic check: does this action target something that eventually leads to admin?
        # This is where we "simulate" the edge
        # For MVP, we'll flag any AssumeRole/PassRole if it's being added to a non-admin
        return True # Conservative approach for guard
