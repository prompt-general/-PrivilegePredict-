#!/bin/bash
# status.sh - Status script for PrivilegePredict

echo "Checking PrivilegePredict status..."

# Check if Docker is being used
if command -v docker &> /dev/null && [ -f "docker-compose.yml" ]; then
    echo "Docker Compose services status:"
    docker-compose ps
else
    echo "Checking local services..."

    # Check if backend is running
    if pgrep -f "uvicorn" > /dev/null; then
        echo "Backend: Running"
    else
        echo "Backend: Not running"
    fi

    # Check if frontend is running
    if pgrep -f "npm run dev" > /dev/null; then
        echo "Frontend: Running"
    else
        echo "Frontend: Not running"
    fi

    # Check if Neo4j is running
    if pgrep -f "neo4j" > /dev/null; then
        echo "Neo4j: Running"
    else
        echo "Neo4j: Not running (or not detected)"
    fi
fi