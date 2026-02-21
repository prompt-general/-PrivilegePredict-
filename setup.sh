#!/bin/bash
# setup.sh - Setup script for PrivilegePredict

echo "Setting up PrivilegePredict..."

# Create necessary directories
echo "Creating directories..."
mkdir -p logs
mkdir -p data

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Initialize git repository if it doesn't exist
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

echo "Setup completed successfully!"
echo ""
echo "To start the application:"
echo "  docker-compose up"
echo ""
echo "Or to run locally:"
echo "  make run-all"