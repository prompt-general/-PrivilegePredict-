# PrivilegePredict Documentation

## Overview

PrivilegePredict is a multi-cloud identity graph platform that models real-world identity relationships across AWS and Azure, enabling visualization of privilege escalation paths and forming the foundation for dynamic analysis, real-time monitoring, and automated remediation.

## Architecture

The system consists of several components:

1. **Cloud Connectors** - Connect to AWS IAM and Azure Entra ID to retrieve identity data
2. **Normalization Engine** - Converts provider-specific schemas to a unified identity model
3. **Graph Database** - Stores identity relationships using Neo4j
4. **Path Analysis Engine** - Computes privilege escalation paths using graph traversal algorithms
5. **API Layer** - Provides RESTful endpoints for querying identities and paths
6. **Web UI** - Interactive visualization of the identity graph and escalation paths

## Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 16+ (for frontend development)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/privilegepredict/privilegepredict.git
   cd privilegepredict
   ```

2. Start all services:
   ```bash
   docker-compose up
   ```

3. Access the services:
   - Web UI: http://localhost:3000
   - API: http://localhost:8000
   - Neo4j Browser: http://localhost:7474 (username: neo4j, password: password)

## API Endpoints

### Identities

- `GET /identities` - List all identities
- `GET /identities/{id}` - Get identity by ID

### Paths

- `GET /paths?source={id}[&target={id}]` - Find escalation paths

### Risk

- `GET /risk/high-risk-identities` - List high-risk identities

## Data Model

### Identity Nodes

Properties:
- `id` (string) - Unique identifier (e.g., "aws::123456789012::user::alice")
- `provider` (string) - Cloud provider ("aws" or "azure")
- `type` (string) - Identity type ("user", "role", "group", "service_principal")
- `name` (string) - Display name
- `account_id` (string) - Cloud account/tenant ID
- `risk_score` (float) - Computed risk score

### Relationship Types

- `MEMBER_OF` - User/Service Principal is member of Group
- `ASSUMES` - Identity can assume Role
- `ATTACHED_POLICY` - Identity has Policy attached
- `TRUSTS` - Role trusts Identity (cross-account trust)

## Development

### Backend Development

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Development

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Testing

Run backend tests:
```bash
cd backend
python -m pytest tests/
```

## Configuration

The application can be configured using environment variables or the `config.ini` file.

### Environment Variables

- `NEO4J_URI` - Neo4j connection URI
- `NEO4J_USER` - Neo4j username
- `NEO4J_PASSWORD` - Neo4j password
- `AWS_ACCESS_KEY_ID` - AWS access key ID
- `AWS_SECRET_ACCESS_KEY` - AWS secret access key
- `AZURE_TENANT_ID` - Azure tenant ID
- `AZURE_CLIENT_ID` - Azure client ID
- `AZURE_CLIENT_SECRET` - Azure client secret

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT