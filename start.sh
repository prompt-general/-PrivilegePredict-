#!/bin/bash
# start.sh - Startup script for PrivilegePredict

echo "Starting PrivilegePredict..."

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "Docker detected. Starting with Docker Compose..."
    docker-compose up
else
    echo "Docker not found. Starting services locally..."

    # Start Neo4j (assuming it's installed locally)
    echo "Starting Neo4j..."
    # neo4j start  # Uncomment if Neo4j is installed locally

    # Start backend
    echo "Starting backend..."
    cd backend
    uvicorn app.main:app --reload &
    cd ..

    # Start frontend
    echo "Starting frontend..."
    cd frontend
    npm run dev &
    cd ..

    echo "Services started!"
    echo "Backend: http://localhost:8000"
    echo "Frontend: http://localhost:3000"
    echo "Neo4j: http://localhost:7474"
fi