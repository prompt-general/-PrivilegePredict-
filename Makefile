# PrivilegePredict Makefile

# Variables
PYTHON := python3
PIP := pip
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Help target
.PHONY: help
help:
	@echo "PrivilegePredict Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make setup            Install dependencies"
	@echo "  make run-backend      Run the backend server"
	@echo "  make run-frontend     Run the frontend server"
	@echo "  make run-all          Run both frontend and backend"
	@echo "  make docker-up        Start all services with Docker Compose"
	@echo "  make docker-down      Stop all services with Docker Compose"
	@echo "  make docker-build     Build Docker images"
	@echo "  make clean            Clean temporary files"

# Setup target
.PHONY: setup
setup:
	$(PIP) install -r backend/requirements.txt
	cd frontend && npm install

# Run backend target
.PHONY: run-backend
run-backend:
	cd backend && $(PYTHON) -m uvicorn app.main:app --reload

# Run frontend target
.PHONY: run-frontend
run-frontend:
	cd frontend && npm run dev

# Run all services target
.PHONY: run-all
run-all:
	@echo "Starting backend and frontend servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo ""
	cd backend && $(PYTHON) -m uvicorn app.main:app --reload & \
	cd frontend && npm run dev

# Docker targets
.PHONY: docker-up
docker-up:
	$(DOCKER_COMPOSE) up

.PHONY: docker-down
docker-down:
	$(DOCKER_COMPOSE) down

.PHONY: docker-build
docker-build:
	$(DOCKER_COMPOSE) build

# Clean target
.PHONY: clean
clean:
	rm -rf *.egg-info/
	rm -rf build/
	rm -rf dist/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete