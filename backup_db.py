#!/usr/bin/env python3
"""
Backup script to export the Neo4j database
"""

import os
import datetime
from neo4j import GraphDatabase

# Neo4j connection details (to be configured via environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def backup_database():
    """Backup the Neo4j database by exporting all nodes and relationships"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    # Create backup directory if it doesn't exist
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Generate timestamp for backup file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"privilegepredict_backup_{timestamp}.cypher")

    with driver.session() as session:
        print(f"Exporting database to {backup_file}...")

        # This is a simplified backup approach
        # In a production environment, you would use Neo4j's built-in backup tools
        with open(backup_file, "w") as f:
            # Export nodes
            nodes_result = session.run("MATCH (n) RETURN n")
            f.write("// Nodes\n")
            for record in nodes_result:
                node = record["n"]
                f.write(f"CREATE {node};\n")

            # Export relationships
            rels_result = session.run("MATCH ()-[r]->() RETURN r")
            f.write("\n// Relationships\n")
            for record in rels_result:
                rel = record["r"]
                f.write(f"CREATE {rel};\n")

        print("Database backup completed successfully!")

    driver.close()

if __name__ == "__main__":
    backup_database()