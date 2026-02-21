#!/usr/bin/env python3
"""
Check script to verify the project structure
"""

import os

def check_project_structure():
    """Check if all required files and directories exist"""
    required_files = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "docker-compose.yml",
        "config.ini",
        "Makefile",
        "setup.sh",
        "start.sh",
        "stop.sh",
        "status.sh",
        "test_services.py",
        "reset_db.py",
        "backup_db.py",
        "restore_db.py",
        "backend/requirements.txt",
        "backend/Dockerfile",
        "backend/app/main.py",
        "backend/app/api/identities.py",
        "backend/app/api/paths.py",
        "backend/app/api/risk.py",
        "backend/app/models/identity.py",
        "backend/app/models/path.py",
        "backend/app/services/identity_service.py",
        "backend/app/services/path_service.py",
        "backend/app/services/risk_service.py",
        "backend/app/graph/database.py",
        "backend/ingestion/aws_connector.py",
        "backend/ingestion/azure_connector.py",
        "backend/ingestion/normalizer.py",
        "backend/ingestion/main.py",
        "backend/scripts/init_db.py",
        "frontend/package.json",
        "frontend/Dockerfile",
        "frontend/vite.config.js",
        "frontend/src/main.jsx",
        "frontend/src/App.jsx",
        "frontend/src/index.css",
        "frontend/src/App.css",
        "frontend/src/components/Navigation.jsx",
        "frontend/src/components/IdentityList.jsx",
        "frontend/src/components/IdentityGraph.jsx",
        "frontend/src/api/index.js"
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("Missing files:")
        for file_path in missing_files:
            print(f"  {file_path}")
        return False
    else:
        print("All required files are present!")
        return True

if __name__ == "__main__":
    check_project_structure()