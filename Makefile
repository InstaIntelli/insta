# ============================================
# INSTAINTELLI - Makefile
# ============================================
# Common Docker and development commands
# Usage: make <command>

.PHONY: help build up down restart logs clean test migrate init-db

# Default target
help:
	@echo "InstaIntelli - Development Commands"
	@echo "===================================="
	@echo "  make build          - Build all Docker images"
	@echo "  make up              - Start all services"
	@echo "  make down            - Stop all services"
	@echo "  make restart         - Restart all services"
	@echo "  make logs             - View logs from all services"
	@echo "  make logs-backend    - View backend logs"
	@echo "  make logs-frontend   - View frontend logs"
	@echo "  make clean            - Remove containers, volumes, and images"
	@echo "  make test             - Run tests in backend container"
	@echo "  make migrate          - Run database migrations"
	@echo "  make init-db          - Initialize all databases"
	@echo "  make shell-backend    - Open shell in backend container"
	@echo "  make shell-postgres   - Open PostgreSQL shell"
	@echo "  make shell-mongodb    - Open MongoDB shell"
	@echo "  make shell-redis     - Open Redis CLI"

# Build all images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Start all services with logs
up-logs:
	docker-compose up

# Stop all services
down:
	docker-compose down

# Stop and remove volumes
down-volumes:
	docker-compose down -v

# Restart all services
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# View backend logs
logs-backend:
	docker-compose logs -f backend

# View frontend logs
logs-frontend:
	docker-compose logs -f frontend

# Clean everything (containers, volumes, images)
clean:
	docker-compose down -v --rmi all

# Run tests
test:
	docker-compose exec backend pytest

# Run database migrations
migrate:
	docker-compose exec backend alembic upgrade head

# Initialize all databases
init-db:
	@echo "Initializing databases..."
	@docker-compose exec -T postgres bash /app/scripts/init_postgres.sh || true
	@docker-compose exec -T mongodb bash /app/scripts/init_mongodb.sh || true
	@echo "Database initialization complete!"

# Open shell in backend container
shell-backend:
	docker-compose exec backend /bin/bash

# Open PostgreSQL shell
shell-postgres:
	docker-compose exec postgres psql -U postgres -d instaintelli

# Open MongoDB shell
shell-mongodb:
	docker-compose exec mongodb mongosh instaintelli

# Open Redis CLI
shell-redis:
	docker-compose exec redis redis-cli

# Rebuild and restart
rebuild:
	docker-compose up -d --build

# Check service health
health:
	@echo "Checking service health..."
	@docker-compose ps
	@echo "\nBackend health:"
	@curl -s http://localhost:8000/health || echo "Backend not responding"
	@echo "\nFrontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"








