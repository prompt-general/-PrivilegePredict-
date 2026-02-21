#!/usr/bin/env python3
"""
Test script to verify PrivilegePredict services
"""

import requests
import time

def test_backend():
    """Test the backend API"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend API: OK")
            return True
        else:
            print("✗ Backend API: Unexpected status code", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend API: Connection failed")
        return False
    except Exception as e:
        print("✗ Backend API:", str(e))
        return False

def test_frontend():
    """Test the frontend server"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✓ Frontend: OK")
            return True
        else:
            print("✗ Frontend: Unexpected status code", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Frontend: Connection failed")
        return False
    except Exception as e:
        print("✗ Frontend:", str(e))
        return False

def test_neo4j():
    """Test Neo4j connection"""
    # This is a simple test - in reality, we'd need the Neo4j driver to properly test
    try:
        response = requests.get("http://localhost:7474", timeout=5)
        if response.status_code == 200:
            print("✓ Neo4j: OK")
            return True
        else:
            print("✗ Neo4j: Unexpected status code", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Neo4j: Connection failed")
        return False
    except Exception as e:
        print("✗ Neo4j:", str(e))
        return False

def main():
    print("Testing PrivilegePredict services...")
    print("=" * 40)

    # Give services a moment to start
    time.sleep(2)

    results = []
    results.append(test_backend())
    results.append(test_frontend())
    results.append(test_neo4j())

    print("=" * 40)
    if all(results):
        print("All services are running correctly!")
        return 0
    else:
        print("Some services are not running correctly.")
        return 1

if __name__ == "__main__":
    exit(main())