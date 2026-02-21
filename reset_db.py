#!/usr/bin/env python3
"""
Reset script to clear the Neo4j database
"""

import os
from neo4j import GraphDatabase

# Neo4j connection details (to be configured via environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def reset_database():
    """Reset the Neo4j database by deleting all nodes and relationships"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        print("Deleting all nodes and relationships...")
        session.run("""
            MATCH (n)
            DETACH DELETE n
        """)

        print("Database reset completed successfully!")

    driver.close()

if __name__ == "__main__":
    confirm = input("This will delete all data in the database. Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
    else:
        print("Database reset cancelled.")