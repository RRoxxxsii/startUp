CONFIG_DEV_LINT_PATH='./backend/.pre-commit.config.yaml'

# Create file with environment variables
create-envs-dev:
	cat envs/.envExampleDev > .env

create-envs-prod:
	cat envs/.envExampleProd > .env

# Build docker images and run for development
build-up-docker-dev:
	docker compose -f docker-compose.dev.yaml up --build

# Run for development
up-docker-dev:
	docker compose -f docker-compose.dev.yaml up

# Build for development
build-docker-dev:
	docker compose -f docker-compose.dev.yaml build


# Build docker images and run for production
build-up-docker-prod:
	docker compose -f docker-compose.prod.yaml up --build

# Run for production
up-docker-prod:
	docker compose -f docker-compose.prod.yaml up

# Build for production
build-docker-prod:
	docker compose -f docker-compose.prod.yaml build

# Run all tests
test:
	pytest -v -s

# Lint
lint:
	cd ./backend && pre-commit run --all-files
