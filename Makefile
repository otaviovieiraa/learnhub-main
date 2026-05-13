.PHONY: help dev prod stop logs build clean test healthcheck

# Default target
help:
	@echo "LearnHub - Docker Commands"
	@echo "=========================="
	@echo ""
	@echo "Development:"
	@echo "  make dev              - Start development environment"
	@echo "  make dev-stop         - Stop development environment"
	@echo "  make dev-logs         - Show development logs"
	@echo "  make dev-build        - Rebuild development image"
	@echo ""
	@echo "Production:"
	@echo "  make prod             - Start production environment"
	@echo "  make prod-stop        - Stop production environment"
	@echo "  make prod-logs        - Show production logs"
	@echo "  make prod-build       - Build production image"
	@echo ""
	@echo "Database:"
	@echo "  make migrate          - Run Django migrations"
	@echo "  make createsuperuser  - Create admin user"
	@echo "  make dbshell          - Access database shell"
	@echo ""
	@echo "Utilities:"
	@echo "  make test             - Run tests"
	@echo "  make clean            - Remove all containers and volumes"
	@echo "  make healthcheck      - Check service health"
	@echo "  make shell            - Access Django shell"
	@echo ""

# Development targets
dev:
	docker-compose up -d

dev-stop:
	docker-compose down

dev-logs:
	docker-compose logs -f web

dev-build:
	docker-compose build --no-cache

dev-shell:
	docker-compose exec web python manage.py shell

# Production targets
prod:
	docker-compose -f docker-compose.prod.yml up -d

prod-stop:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f web

prod-build:
	docker build --no-cache -t learnhub:latest .

# Database targets
migrate:
	docker-compose exec web python manage.py migrate

migrate-dev:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

dbshell:
	docker-compose exec postgres psql -U postgres -d learnhub_db

# Utility targets
test:
	docker-compose exec web python manage.py test

shell:
	docker-compose exec web python manage.py shell

clean:
	docker-compose down -v
	docker-compose -f docker-compose.prod.yml down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

healthcheck:
	@echo "Checking web service..."
	@curl -s http://localhost:3000/health/ | python -m json.tool || echo "Web service unhealthy"
	@echo ""
	@echo "Checking database..."
	@docker-compose exec -T postgres pg_isready -U postgres || echo "Database unhealthy"

staticfiles:
	docker-compose exec web python manage.py collectstatic --noinput

requirements:
	docker-compose exec web pip freeze > requirements.txt

# Aliases
start: dev
stop: dev-stop
restart: dev-stop dev
logs: dev-logs
