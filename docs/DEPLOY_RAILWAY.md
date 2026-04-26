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
PAYMENTS_ENABLED=true
PAYMENTS_DEFAULT_PROVIDER=telegram_stars
PAYMENTS_ENABLE_TELEGRAM_STARS=true
PAYMENTS_ENABLE_HALYK=false
PAYMENTS_ENABLE_FREEDOM=false
PAYMENTS_ENABLE_KASPI=false
PAYMENTS_ENABLE_CRYPTO=false
PREMIUM_DAILY_FORECAST_LIMIT=50
PREMIUM_DAILY_AI_LIMIT=100
HALYK_EPAY_ENABLED=false
HALYK_EPAY_TEST_MODE=true
HALYK_EPAY_TERMINAL_ID=
HALYK_EPAY_CLIENT_ID=
HALYK_EPAY_CLIENT_SECRET=
HALYK_EPAY_SUCCESS_URL=
HALYK_EPAY_FAILURE_URL=
FREEDOM_PAY_ENABLED=false
FREEDOM_PAY_TEST_MODE=true
FREEDOM_PAY_MERCHANT_ID=
FREEDOM_PAY_SECRET_KEY=
FREEDOM_PAY_RESULT_URL=
FREEDOM_PAY_SUCCESS_URL=
FREEDOM_PAY_FAILURE_URL=
KASPI_ENABLED=false
KASPI_PROVIDER=
KASPI_API_URL=
KASPI_API_KEY=
KASPI_WEBHOOK_SECRET=
CRYPTO_ENABLED=false
CRYPTO_PROVIDER=
CRYPTO_API_KEY=
CRYPTO_WEBHOOK_SECRET=
CRYPTO_ALLOWED_ASSETS=USDT,TON
CRYPTO_NETWORKS=TON,TRC20
SUPPORT_EMAIL=
SUPPORT_TELEGRAM_USERNAME=
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
SUPPORT_EMAIL=
SUPPORT_TELEGRAM_USERNAME=
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
- Telegram Stars is the default in-Telegram payment method for digital access
- External providers stay disabled until their credentials and webhook verification are configured
- Never store card data, crypto private keys, or grant access from screenshots
