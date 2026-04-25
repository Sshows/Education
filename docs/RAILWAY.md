# Railway deployment guide

## Target architecture
Create separate Railway services (do **not** deploy docker-compose as a single service):

1. `api` (public)
2. `web` (public)
3. `bot` (public if Telegram webhook hits this service)
4. `worker` (private)
5. PostgreSQL plugin/service (private)
6. Redis plugin/service (private)

## Config-as-code files
Use these config paths in Railway dashboard service settings:

- `/railway/api.railway.json`
- `/railway/web.railway.json`
- `/railway/bot.railway.json`
- `/railway/worker.railway.json`

> Important: Railway config path is repository-relative and must be set explicitly per service.

## Service setup matrix

### API
- Root directory: `apps/api`
- Dockerfile: `apps/api/Dockerfile`
- Public domain: enabled
- Healthcheck: `/health`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Web
- Root directory: `apps/web`
- Dockerfile: `apps/web/Dockerfile`
- Public domain: enabled
- Healthcheck: `/`
- Start command: `npm run start -- -H 0.0.0.0 -p $PORT`

### Bot
- Root directory: `apps/bot`
- Dockerfile: `apps/bot/Dockerfile`
- Public domain: enabled (for Telegram webhook)
- Healthcheck: `/health`
- Start command: `python -m app.webhook`

### Worker
- Root directory: `apps/worker`
- Dockerfile: `apps/worker/Dockerfile`
- Public domain: disabled
- Start command: `python -m app.worker`

## Required environment variables

Set on `api`, `bot`, `worker`:
- `DATABASE_URL` (from Railway Postgres)
- `REDIS_URL` (from Railway Redis)
- `ENVIRONMENT=production`
- `DEBUG=false`

Set on `api` + `bot`:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`

Set on `api`:
- `SESSION_SECRET`
- `JWT_SECRET`
- `OPENAI_API_KEY` (optional)

Set on `web`:
- `NEXT_PUBLIC_API_URL` (public URL of api service)

Set on `bot`:
- `TELEGRAM_WEBAPP_URL` (public URL of web service)

## Telegram webhook wiring

1. Deploy bot service and get public URL, e.g. `https://bot-production.up.railway.app`.
2. Configure webhook:

```bash
curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook" \
  -d "url=https://<bot-domain>/bot/webhook" \
  -d "secret_token=<TELEGRAM_WEBHOOK_SECRET>"
```

3. Verify:

```bash
curl "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getWebhookInfo"
```

## Notes
- Postgres/Redis should stay private.
- Run migrations as a one-off command in `api` service:
  `alembic upgrade head`
- Optionally seed demo data:
  `python -m app.scripts.seed_sources`
