# ent-grant-telegram

Production-oriented MVP: Telegram Mini App + Telegram Bot + FastAPI backend + ingestion worker для оценки шансов поступления по ЕНТ (грант/платное) с прозрачными источниками.

## Requirements
- Docker + Docker Compose
- Node.js 22+ (для запуска web без Docker)
- Python 3.11+ (для запуска backend без Docker)
- Telegram Bot token (BotFather)

## Quick start
```bash
cp .env.example .env
make up
make migrate
make seed
```

## Local URLs
- Web: http://localhost:3000
- API docs: http://localhost:8000/docs
- API health: http://localhost:8000/health
- API health (namespaced): http://localhost:8000/api/health

## One-command run
```bash
docker compose -f infra/docker-compose.yml up --build
```

## Telegram setup
1. В BotFather: `/newbot`, получите `TELEGRAM_BOT_TOKEN`.
2. Mini App URL: `/setmenubutton` -> `TELEGRAM_WEBAPP_URL`.
3. Для webhook:
```bash
curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook" \
  -d "url=<TELEGRAM_WEBHOOK_URL>" \
  -d "secret_token=<TELEGRAM_WEBHOOK_SECRET>"
```
4. Для локальной проверки webhook используйте ngrok:
```bash
ngrok http 8080
```

## Testing
```bash
make api-test
make web-build
python -m compileall apps/api/app apps/bot/app apps/worker/app
```

## Data pipeline
- Seed базовых источников и демонстрационных записей:
```bash
make seed
# или
cd apps/api && python -m app.scripts.seed_sources
```
- Добавление source: `POST /api/admin/sources` (расширяемый endpoint).
- Fetch source: `POST /api/admin/sources/{id}/fetch`.
- Parse source: `POST /api/admin/sources/{id}/parse`.
- Conflicts: `GET /api/admin/conflicts`.

## Security & production notes
- Только HTTPS в production.
- Backend валидирует Telegram initData.
- Webhook защищён `TELEGRAM_WEBHOOK_SECRET`.
- Добавьте rate-limiting, backups, мониторинг и ротацию секретов.
- Соблюдайте privacy policy: храните минимум персональных данных.

## Product integrity rules
- Прогноз не является гарантией поступления.
- Не показывать числа без источников (или показывать `нет подтверждённых данных`).
- При конфликте источников показывать предупреждение и снижать confidence.
- Максимальная вероятность ограничена 99%.

## Railway deployment
Подробный гайд: `docs/DEPLOY_RAILWAY.md` (legacy notes: `docs/RAILWAY.md`).

Config-as-code файлы:
- `/railway/api.railway.json`
- `/railway/web.railway.json`
- `/railway/bot.railway.json`
- `/railway/worker.railway.json`

Каждый Railway service должен использовать **свой** config path и **свой** Dockerfile. Не деплойте `infra/docker-compose.yml` как единый service.
