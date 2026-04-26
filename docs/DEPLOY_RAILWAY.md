# ENT Grant KZ — Railway Deploy Guide

## Services

| Service | Start command | Port |
|---------|-------------|------|
| `web` | `npm run start` (Next.js) | 3000 |
| `api` | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | $PORT |
| `bot` | `uvicorn app.webhook:app --host 0.0.0.0 --port $PORT` | $PORT |
| `worker` | `python -m app.worker` | — |

## Environment Variables

### Web service

```
NEXT_PUBLIC_API_URL=https://API_DOMAIN
NEXT_PUBLIC_TELEGRAM_BOT_USERNAME=entgrant_kz_bot
NODE_ENV=production
```

### API service

```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ENVIRONMENT=production
DEBUG=false
SESSION_SECRET=<random 32+ chars>
TELEGRAM_BOT_TOKEN=<from @BotFather — Railway Variables only, never commit>
OPENAI_API_KEY=<optional>
```

### Bot service

```
TELEGRAM_BOT_TOKEN=<from @BotFather — Railway Variables only>
TELEGRAM_WEBAPP_URL=https://ent-grant-web-production.up.railway.app
TELEGRAM_WEBHOOK_URL=https://BOT_DOMAIN/webhook
TELEGRAM_WEBHOOK_SECRET=<random 32+ chars>
TELEGRAM_AUTO_SET_WEBHOOK=true
TELEGRAM_AUTO_SET_MENU_BUTTON=true
TELEGRAM_AUTO_SET_COMMANDS=true
API_URL=https://API_DOMAIN
ENVIRONMENT=production
```

### Worker service

```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
API_URL=https://API_DOMAIN
ENVIRONMENT=production
```

## Webhook verification

After deploying the bot:

```bash
curl https://BOT_DOMAIN/health
# {"status":"ok","service":"bot"}

curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
# Check url, last_error_date
```

## Domains

- Web: Railway auto-assigns `*.up.railway.app` or use custom domain
- Bot: Must have a public HTTPS domain (required for Telegram webhook)
- `TELEGRAM_WEBAPP_URL` must point to the **web** service domain  
- `TELEGRAM_WEBHOOK_URL` must point to the **bot** service domain

## Redeploy steps

1. Push to `origin main`
2. Railway auto-deploys if connected to GitHub  
   Or: Run `railway up` from the service directory
3. Check logs: `railway logs --tail`
4. Verify webhook: see above

## Security notes

- Never hardcode `TELEGRAM_BOT_TOKEN` — add it only in Railway Variables UI
- `TELEGRAM_WEBHOOK_SECRET` must be set in production (validated on every request)
- Frontend never gets the token
