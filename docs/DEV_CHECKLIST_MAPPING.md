# Customer dev checklist mapping

Source: `dev checklist.pdf` from the customer.

## Implemented in this repo

- Telegram Mini App runs as `apps/web` on Railway.
- Bot webhook runs as `apps/bot` with `/health`, `/webhook`, commands and Telegram Web App buttons.
- Product API exposes `GET /api/specialties?subject=math_cs`.
- Product API exposes `POST /api/analyze`.
- First analysis per Telegram user is free through `users.free_analysis_used`.
- Repeated analysis returns `paywall=true` unless `pro_once` or `premium_month` entitlement exists.
- Analysis requests are stored in `analyses` for audit and future card generation.
- Telegram Stars payment flow is the primary in-Telegram checkout.
- AiPay compatibility endpoints exist as disabled-by-default external checkout:
  - `POST /api/payment/create`
  - `POST /api/payment/webhook`
  - `POST /api/payments/webhooks/aipay`
- Result page has Telegram sharing through `https://t.me/share/url`.

## Intentionally adapted

- The PDF describes VPS, Nginx and Docker Compose production. This project uses Railway production services, so VPS steps are documented only as infrastructure context.
- The PDF names AiPay as the payment provider. This repo keeps Telegram Stars primary inside Telegram and exposes AiPay as an external KZT adapter behind feature flags.
- PNG card generation is queued in the API response as `card_status`, but full Puppeteer/Chromium card rendering is still a later worker task.

## Manual checks after Railway deploy

```bash
curl "https://API_DOMAIN/api/specialties?subject=math_cs"
curl -X POST "https://API_DOMAIN/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"tg_id":123456789,"score":110,"subject_pair":"math_cs","quota":"general","spec_codes":["B057","B058"]}'
curl "https://BOT_DOMAIN/health"
```

Then open `@entgrant_kz_bot`, send `/start`, open calculator, run one analysis, and share the result from the result page.
