#!/bin/bash
# stop.sh - Stop script for PrivilegePredict

echo "Stopping PrivilegePredict..."

# Check if Docker is being used
if command -v docker &> /dev/null && [ -f "docker-compose.yml" ]; then
    echo "Stopping Docker Compose services..."
    docker-compose down
else
    echo "Stopping local services..."
    # Kill background processes
    pkill -f "uvicorn"
    pkill -f "npm run dev"
    # Stop Neo4j if it's running locally
    # neo4j stop  # Uncomment if Neo4j is installed locally
fi

echo "Services stopped!"