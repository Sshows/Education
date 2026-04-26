# ent-grant-telegram

Telegram-first MVP for Kazakhstan applicants: Telegram Mini App, aiogram bot, FastAPI backend, and worker jobs for education data ingestion.

## Structure

- `apps/web` - Next.js 15 Telegram Mini App.
- `apps/api` - FastAPI, SQLAlchemy, Alembic, Telegram `initData` auth.
- `apps/bot` - aiogram v3 webhook bot for Railway.
- `apps/worker` - RQ worker for ingestion/recalculation jobs.
- `packages/shared` - shared constants.
- `infra` - local docker-compose and nginx.
- `railway` - Railway service config examples.
- `docs` - architecture and deployment runbooks.

## Production URLs

- Web: `https://ent-grant-web-production.up.railway.app`
- Bot: `@entgrant_kz_bot`
- API/Bot domains: generated in Railway per service.

## Local start

```bash
docker compose -f infra/docker-compose.yml up --build
```

Services:

- API: `http://localhost:8000`
- Web: `http://localhost:3000`
- Bot webhook server: `http://localhost:8080`
- Postgres: `localhost:5432`
- Redis: `localhost:6379`

## Telegram and Railway setup

Read:

- [Telegram setup](docs/TELEGRAM_SETUP.md)
- [Railway deployment](docs/DEPLOY_RAILWAY.md)
- [Payments architecture](docs/PAYMENTS.md)
- [Telegram Stars](docs/TELEGRAM_STARS.md)
- [Payment providers](docs/PAYMENT_PROVIDERS.md)

The bot token must live only in Railway Variables or local untracked `.env` files. If a token is exposed, rotate it in BotFather before production use.

## Checks

```bash
python -m compileall apps/api/app apps/bot/app apps/worker/app
cd apps/api && pytest -q
cd ../web && npm run build
```

## Product safety rules

- A forecast is not an admission or grant guarantee.
- Every important number should link to a source, publisher, fetch date, and confidence.
- If data is missing, show that confirmed source data is unavailable.
- Do not trust Telegram user IDs from the frontend until `/api/auth/telegram` validates `initData`.
- Telegram Stars is primary for digital access inside Telegram.
- External KZT/crypto providers are feature-flagged and must verify provider status/webhooks before access is granted.
