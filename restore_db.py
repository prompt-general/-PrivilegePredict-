#!/usr/bin/env python3
"""
Restore script to import data into the Neo4j database
"""

import os
import sys
from neo4j import GraphDatabase

# Neo4j connection details (to be configured via environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def restore_database(backup_file):
    """Restore the Neo4j database from a backup file"""
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} not found!")
        return

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        print(f"Importing database from {backup_file}...")

        # Read and execute the backup file
        with open(backup_file, "r") as f:
            cypher_commands = f.read().split(";")

            for command in cypher_commands:
                command = command.strip()
                if command and not command.startswith("//"):
                    try:
                        session.run(command)
                    except Exception as e:
                        print(f"Warning: Failed to execute command: {command[:50]}... Error: {e}")

        print("Database restore completed successfully!")

    driver.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python restore_db.py <backup_file>")
        sys.exit(1)

    backup_file = sys.argv[1]
    restore_database(backup_file)