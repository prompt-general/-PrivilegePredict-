#!/bin/bash
# full_test.sh - Complete setup and test script for PrivilegePredict

echo "Running complete PrivilegePredict setup and test..."

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "Error: Please run this script from the PrivilegePredict root directory"
    exit 1
fi

# Run project structure check
echo "Checking project structure..."
python check_structure.py

# Run setup script
echo "Running setup..."
./setup.sh

# Run service test
echo "Testing services..."
python test_services.py

echo "Complete setup and test finished!"
echo ""
echo "To start the application, run:"
echo "  ./start.sh"
echo ""
echo "To check status, run:"
echo "  ./status.sh"
echo ""
echo "To stop the application, run:"
echo "  ./stop.sh"