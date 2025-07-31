# Makefile for Django Project (Dockerized)

# Variables
PYTHON=python
PIP=pip
MANAGE=$(PYTHON) src/manage.py
VENV=.venv
DOCKER_COMPOSE=docker-compose
DOCKER_COMPOSE_FILE=docker-compose.yml
WEB=web  # Change if your Django service is named differently

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  venv                Create virtual environment"
	@echo "  install             Install dependencies"
	@echo "  migrate             Run Django migrations"
	@echo "  createsuperuser     Create a Django superuser"
	@echo "  run                 Run the development server"
	@echo "  test                Run all tests"
	@echo "  lint                Run flake8 linter"
	@echo "  shell               Open Django shell"
	@echo "  clean               Remove .pyc files and __pycache__"
	@echo "  docker-build        Build Docker images"
	@echo "  docker-up           Start all Docker containers"
	@echo "  docker-down         Stop all Docker containers"
	@echo "  docker-logs         Show logs from Docker containers"
	@echo "  docker-bash         Open a bash shell in the Django container"
	@echo "  makemessages        Extract translation strings"
	@echo "  compilemessages     Compile translation files"
	@echo "  collectstatic       Collect static files"
	@echo "  makemigrations      Create new migrations"
	@echo "  deploy              Deploy the app (customize as needed)"

# Create virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV)

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Run migrations
.PHONY: migrate
migrate:
	$(MANAGE) migrate

# Create superuser
.PHONY: createsuperuser
createsuperuser:
	$(MANAGE) createsuperuser

# Run development server
.PHONY: run
run:
	$(MANAGE) runserver 0.0.0.0:8000

# Run tests
.PHONY: test
test:
	$(MANAGE) test

# Lint code
.PHONY: lint
lint:
	flake8 src/

# Open Django shell
.PHONY: shell
shell:
	$(MANAGE) shell

# Clean up .pyc and __pycache__
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +

# Docker commands
.PHONY: docker-build
docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

.PHONY: docker-up
docker-up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

.PHONY: docker-down
docker-down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

.PHONY: docker-logs
docker-logs:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f

.PHONY: docker-bash
docker-bash:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(WEB) bash

# Translation commands (run inside the Django container)
.PHONY: makemessages
makemessages:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(WEB) python manage.py makemessages -l fr -l es

.PHONY: compilemessages
compilemessages:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(WEB) python manage.py compilemessages

# Static/media management
.PHONY: collectstatic
collectstatic:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(WEB) python manage.py collectstatic --noinput

.PHONY: makemigrations
makemigrations:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) exec $(WEB) python manage.py makemigrations

# Deployment (customize as needed)
.PHONY: deploy
deploy:
	@echo "Add your deployment steps here (e.g., push to server, run migrations, collectstatic, restart services, etc.)" 