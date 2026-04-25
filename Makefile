COMPOSE=docker compose -f infra/docker-compose.yml

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f --tail=200

api-test:
	cd apps/api && pytest -q

web-build:
	cd apps/web && npm install && npm run build

seed:
	cd apps/api && python -m app.scripts.seed_sources

migrate:
	cd apps/api && alembic upgrade head

lint:
	cd apps/web && npm run lint || true

format:
	python -m compileall apps/api/app apps/bot/app apps/worker/app
