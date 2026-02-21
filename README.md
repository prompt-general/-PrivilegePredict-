# PrivilegePredict

PrivilegePredict is a multi-cloud identity graph platform that models real-world identity relationships across AWS and Azure, enabling visualization of privilege escalation paths and forming the foundation for dynamic analysis, real-time monitoring, and automated remediation.

## Features

- Ingest AWS IAM data (Users, Roles, Groups, Policies, Trust relationships)
- Ingest Azure Entra ID data (Users, Groups, Service Principals, Role Assignments)
- Normalize identities into a unified graph model
- Store relationships in graph database (Neo4j)
- Compute privilege escalation paths using graph traversal
- Provide basic web UI for graph visualization and path exploration
- CLI tool for data ingestion
- Export graph in JSON for API consumption

## Architecture

```
PrivilegePredict/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   ├── graph/
│   │   └── models/
│   ├── ingestion/
│   │   ├── aws_connector.py
│   │   ├── azure_connector.py
│   │   └── normalizer.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 16+ (for frontend development)

### Quick Start

1. Clone the repository
2. Run `docker-compose up` to start the services
3. Access the web UI at http://localhost:3000

### Development Setup

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- GET /identities - List all identities
- GET /identities/{id} - Get identity by ID
- GET /paths?source={id}&target={id} - Get escalation paths
- GET /high-risk-identities - List high-risk identities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT