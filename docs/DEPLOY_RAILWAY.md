# Deploy to Railway (Monorepo)

> Railway must run **4 separate services** from this monorepo: `web`, `api`, `bot`, `worker`.
> Do **not** deploy `docker-compose` as one service.

## A) Create Railway project
1. Create a new Railway Project.
2. Connect this GitHub repository.

## B) Add PostgreSQL
1. Add Railway PostgreSQL plugin/service.
2. Ensure `DATABASE_URL` is shared to `api`, `bot`, `worker`.

## C) Add Redis
1. Add Railway Redis plugin/service.
2. Ensure `REDIS_URL` is shared to `api`, `bot`, `worker`.

## D) Create service `api`
- Root Directory: `apps/api`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Healthcheck: `/health`

Variables:
- `DATABASE_URL`
- `REDIS_URL`
- `SESSION_SECRET`
- `ENVIRONMENT=production`
- `DEBUG=false`
- `OPENAI_API_KEY` (optional)

## E) Create service `web`
- Root Directory: `apps/web`
- Start Command: `npm run start -- -p $PORT`
- Healthcheck: `/`

Variables:
- `NEXT_PUBLIC_API_URL=https://api-service-domain`
- `NODE_ENV=production`

## F) Create service `bot`
- Root Directory: `apps/bot`
- Start Command: `python -m app.webhook`

Variables:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBAPP_URL=https://web-service-domain`
- `TELEGRAM_WEBHOOK_URL=https://bot-service-domain/webhook`
- `TELEGRAM_WEBHOOK_SECRET`
- `API_URL=https://api-service-domain`

## G) Create service `worker`
- Root Directory: `apps/worker`
- Start Command: `python -m app.worker`

Variables:
- `DATABASE_URL`
- `REDIS_URL`
- `API_URL=https://api-service-domain`

## H) Run seed on Railway
From API service shell or Railway CLI:

```bash
railway run python -m app.scripts.seed_sources
```

## I) Verify deployment
- `https://api-domain/health`
- `https://api-domain/docs`
- `https://web-domain`
- Telegram command `/start`

## J) Troubleshooting
- If Railway installs Node in `api/bot/worker`: wrong **Root Directory**.
- If app fails on port: hardcoded port, must bind `$PORT`.
- If `DATABASE_URL` missing: attach PostgreSQL vars.
- If `REDIS_URL` missing: attach Redis vars.
- If web cannot reach API: check `NEXT_PUBLIC_API_URL`.
- If Mini App not opening: check `TELEGRAM_WEBAPP_URL` and HTTPS.
- If webhook fails: check `TELEGRAM_WEBHOOK_URL` + `TELEGRAM_WEBHOOK_SECRET`.

## Config file paths
Set per-service config path explicitly:
- `/railway/api.railway.json`
- `/railway/web.railway.json`
- `/railway/bot.railway.json`
- `/railway/worker.railway.json`
