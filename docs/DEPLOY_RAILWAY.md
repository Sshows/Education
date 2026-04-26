# Railway deployment

This project is a Railway monorepo. Create one Railway service per app and set Root Directory explicitly.

## Services

| Service | Root Directory | Start Command | Public URL |
| --- | --- | --- | --- |
| `ent-grant-web` | `apps/web` | `npm run start -- -p $PORT` | `https://ent-grant-web-production.up.railway.app` |
| `ent-grant-api` | `apps/api` | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | Railway generated domain |
| `ent-grant-bot` | `apps/bot` | `python -m app.webhook` | Railway generated domain |
| `ent-grant-worker` | `apps/worker` | `python -m app.worker` | private worker |
| `PostgreSQL` | Railway plugin | managed | internal |
| `Redis` | Railway plugin | managed | internal |

If Railway builds the wrong stack, the Root Directory is usually wrong. Set the service Root Directory above, or set `RAILWAY_DOCKERFILE_PATH=Dockerfile` for the service.

Railway config files are in:

```text
railway/api.railway.json
railway/web.railway.json
railway/bot.railway.json
railway/worker.railway.json
```

## Variables

### ent-grant-web

```text
NEXT_PUBLIC_API_URL=https://ENT_GRANT_API_DOMAIN
NEXT_PUBLIC_TELEGRAM_BOT_USERNAME=entgrant_kz_bot
NODE_ENV=production
```

### ent-grant-api

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
ENVIRONMENT=production
DEBUG=false
SESSION_SECRET=generate_long_random_secret
TELEGRAM_BOT_TOKEN=same_bot_token_for_initdata_validation
OPENAI_API_KEY=optional
```

### ent-grant-bot

```text
TELEGRAM_BOT_TOKEN=token_from_BotFather
TELEGRAM_WEBAPP_URL=https://ent-grant-web-production.up.railway.app
TELEGRAM_WEBHOOK_URL=https://ENT_GRANT_BOT_DOMAIN/webhook
TELEGRAM_WEBHOOK_SECRET=generate_long_random_secret
TELEGRAM_AUTO_SET_WEBHOOK=true
TELEGRAM_AUTO_SET_MENU_BUTTON=true
TELEGRAM_AUTO_SET_COMMANDS=true
API_URL=https://ENT_GRANT_API_DOMAIN
ENVIRONMENT=production
```

### ent-grant-worker

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
API_URL=https://ENT_GRANT_API_DOMAIN
ENVIRONMENT=production
```

## Deploy sequence

1. Create PostgreSQL and Redis in Railway.
2. Create `ent-grant-api`, Root Directory `apps/api`, generate domain, add variables.
3. Create `ent-grant-web`, Root Directory `apps/web`, add `NEXT_PUBLIC_API_URL`, deploy.
4. Create `ent-grant-bot`, Root Directory `apps/bot`, generate domain.
5. Set `TELEGRAM_WEBHOOK_URL=https://ENT_GRANT_BOT_DOMAIN/webhook`.
6. Set `TELEGRAM_AUTO_SET_WEBHOOK=true` and redeploy bot.
7. Create `ent-grant-worker`, Root Directory `apps/worker`, add Redis/Postgres variables.

## Post-deploy checks

```text
https://ENT_GRANT_API_DOMAIN/health
https://ENT_GRANT_API_DOMAIN/docs
https://ent-grant-web-production.up.railway.app
https://ENT_GRANT_BOT_DOMAIN/health
```

Then:

```bash
bash scripts/get_telegram_webhook_info.sh
```

Finally open Telegram and send:

```text
/start
```

## Security

- Never commit `.env`.
- Never commit or log `TELEGRAM_BOT_TOKEN`.
- Production bot webhook requires `TELEGRAM_WEBHOOK_SECRET`.
- Frontend Telegram user data is not trusted until backend validates `initData`.
- Use HTTPS for `TELEGRAM_WEBAPP_URL` and `TELEGRAM_WEBHOOK_URL`.
