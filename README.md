# ent-grant-telegram

Telegram-first MVP для абитуриентов Казахстана: Mini App + Telegram Bot + AI-консультант по поступлению на грант/платное.

## Monorepo структура

- `apps/web` — Next.js 15 Mini App (mobile-first).
- `apps/api` — FastAPI + SQLAlchemy + Alembic + Redis.
- `apps/bot` — aiogram v3 webhook bot.
- `apps/worker` — worker для ingestion и пересчётов.
- `packages/shared` — shared types/constants.
- `infra` — docker-compose + nginx.
- `docs` — ERD, runbook, architecture.

## Быстрый старт (Docker)

```bash
docker compose -f infra/docker-compose.yml up --build
```

Сервисы:
- API: `http://localhost:8000`
- Web: `http://localhost:3000`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

## Как создать Telegram bot (BotFather)

1. Открыть `@BotFather`.
2. `/newbot` и получить token.
3. Указать token в `.env` как `TELEGRAM_BOT_TOKEN`.
4. Настроить Web App URL в BotFather (`/setmenubutton`) на `https://<domain>`.

## Как настроить Mini App URL

- `NEXT_PUBLIC_TELEGRAM_BOT_USERNAME` и `TELEGRAM_MINI_APP_URL` должны указывать на production HTTPS URL.
- В `apps/bot/app/bot.py` кнопка WebApp открывает Mini App.

## Как установить webhook

```bash
curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook" \
  -d "url=https://<domain>/bot/webhook" \
  -d "secret_token=<TELEGRAM_WEBHOOK_SECRET>"
```

## Seed sources

```bash
python -m apps.api.app.scripts.seed_sources
```

## Run ingestion

```bash
python -m apps.worker.app.worker
```

## Run tests

```bash
cd apps/api && pytest
cd ../../apps/web && npm test
```

## Deploy

1. Поднять Postgres/Redis.
2. Прогнать Alembic миграции.
3. Деплой API + bot webhook за reverse proxy (HTTPS).
4. Деплой web (Next.js) и связать URL в Telegram.
5. Включить rate limiting и мониторинг.

## Product safety rules

- Прогноз не является гарантией поступления.
- Каждая цифра должна иметь источник, издателя, дату загрузки, confidence.
- Если источника нет: `нет подтверждённых данных`.
