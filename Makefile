.PHONY: help build up down logs restart clean test shell

# Default target
help:
	@echo "Emergent AI Compliance - Docker Commands"
	@echo ""
	@echo "Development:"
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs (all services)"
	@echo "  make logs-backend - View backend logs"
	@echo "  make logs-frontend - View frontend logs"
	@echo "  make logs-db     - View MongoDB logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean       - Remove containers and volumes"
	@echo "  make clean-all   - Remove everything including images"
	@echo "  make shell-backend - Access backend container shell"
	@echo "  make shell-db    - Access MongoDB shell"
	@echo "  make ps          - Show running containers"
	@echo ""
	@echo "Production:"
	@echo "  make prod-up     - Start production environment"
	@echo "  make prod-down   - Stop production environment"
	@echo "  make prod-logs   - View production logs"

# Development commands
build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting services..."
	docker-compose up -d
	@echo ""
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8001"
	@echo "API Docs: http://localhost:8001/docs"

down:
	@echo "Stopping services..."
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f mongodb

ps:
	docker-compose ps

# Maintenance commands
clean:
	@echo "Removing containers and volumes..."
	docker-compose down -v

clean-all:
	@echo "Removing everything..."
	docker-compose down -v --rmi all

shell-backend:
	docker-compose exec backend bash

shell-db:
	docker-compose exec mongodb mongosh

# Testing
test-backend:
	docker-compose exec backend python3 -m pytest

test-api:
	@echo "Testing API endpoints..."
	curl -f http://localhost:8001/api/ || (echo "Backend not running!" && exit 1)
	@echo "✓ Backend API is running"

# Production commands
prod-up:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Production services started!"

prod-down:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-restart:
	@$(MAKE) prod-down
	@$(MAKE) prod-up

# Database management
db-backup:
	@echo "Creating database backup..."
	docker exec emergent-compliance-mongodb mongodump --out /data/backup/$$(date +%Y%m%d_%H%M%S)
	@echo "Backup created!"

db-shell:
	docker exec -it emergent-compliance-mongodb mongosh compliance_db

# Health check
health:
	@echo "Checking service health..."
	@docker inspect --format='{{.State.Health.Status}}' emergent-compliance-backend 2>/dev/null || echo "Backend: not running"
	@docker inspect --format='{{.State.Health.Status}}' emergent-compliance-mongodb 2>/dev/null || echo "MongoDB: not running"
	@docker inspect --format='{{.State.Health.Status}}' emergent-compliance-frontend 2>/dev/null || echo "Frontend: not running"

# Complete setup (first time)
setup: build up
	@echo ""
	@echo "Waiting for services to be ready..."
	@sleep 10
	@$(MAKE) health
	@echo ""
	@echo "Setup complete! Access the app at http://localhost:3000"
