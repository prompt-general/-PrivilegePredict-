from neo4j import GraphDatabase
import os

# Neo4j connection details (to be configured via environment variables)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class DatabaseConnection:
    def __init__(self):
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self._driver.close()

    def get_driver(self):
        return self._driver

# Singleton instance
_db_connection = None

def get_db_connection():
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection

def close_db_connection():
    global _db_connection
    if _db_connection is not None:
        _db_connection.close()
        _db_connection = None