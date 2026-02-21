#!/usr/bin/env python3
"""
Initialize Neo4j database with constraints and indexes
"""

import os
from neo4j import GraphDatabase

# Neo4j connection details (to be configured via environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

def init_database():
    """Initialize the Neo4j database with constraints and indexes"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        # Create constraints
        print("Creating constraints...")
        session.run("""
            CREATE CONSTRAINT identity_id IF NOT EXISTS
            FOR (i:Identity) REQUIRE i.id IS UNIQUE
        """)

        session.run("""
            CREATE CONSTRAINT policy_id IF NOT EXISTS
            FOR (p:Policy) REQUIRE p.id IS UNIQUE
        """)

        # Create indexes
        print("Creating indexes...")
        session.run("""
            CREATE INDEX permission_action IF NOT EXISTS
            FOR (p:Permission) ON (p.action)
        """)

        session.run("""
            CREATE INDEX identity_provider IF NOT EXISTS
            FOR (i:Identity) ON (i.provider)
        """)

        session.run("""
            CREATE INDEX identity_type IF NOT EXISTS
            FOR (i:Identity) ON (i.type)
        """)

        print("Database initialization completed successfully!")

    driver.close()

if __name__ == "__main__":
    init_database()