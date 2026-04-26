# Telegram Mini App setup

Bot username: `@entgrant_kz_bot`

Production Web URL:

```text
https://ent-grant-web-production.up.railway.app
```

Do not commit or paste `TELEGRAM_BOT_TOKEN`. Store it only in Railway Variables and rotate it in BotFather if it was exposed anywhere.

## BotFather checklist

Open `@BotFather` in Telegram.

1. `/newbot`
   - Create the bot.
   - Copy the token into Railway Variables only.

2. `/setdescription`

```text
Оцените шанс поступления на грант или платное обучение по ЕНТ. Прогноз основан на открытых источниках и не является гарантией.
```

3. `/setabouttext`

```text
Калькулятор ЕНТ, вузы, гранты и AI-консультант.
```

4. `/setcommands`

```text
start - Запустить бота
calc - Рассчитать шанс
programs - Программы
universities - Вузы
deadlines - Дедлайны
profile - Профиль
ask - AI-консультант
sources - Источники
premium - Premium и оплата Stars
buy - Купить полный прогноз
payments - Мои платежи
restore - Восстановить доступ
support - Поддержка
help - Помощь
```

5. If BotFather offers Mini App settings:
   - URL: `https://ent-grant-web-production.up.railway.app`
   - Short name: `entgrant`
   - Title: `ENT Grant`

The Mini App also works through `InlineKeyboardButton.web_app` and `setChatMenuButton`, so `/newapp` is optional.

## Railway bot variables

Set these on `ent-grant-bot`:

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

Set the same bot token on `ent-grant-api` as `TELEGRAM_BOT_TOKEN` so `/api/auth/telegram` can validate Mini App `initData`.

## How the bot works

`/start` sends:

```text
Привет! Я помогу оценить шанс поступления на грант или платное обучение по ЕНТ. Расчёт не является официальной гарантией, но использует открытые источники и исторические данные.
```

Then it shows Telegram Web App buttons:

- `Рассчитать шанс` -> `{TELEGRAM_WEBAPP_URL}/calculator`
- `Подобрать вуз` -> `{TELEGRAM_WEBAPP_URL}/universities`
- `Программы` -> `{TELEGRAM_WEBAPP_URL}/programs`
- `Спросить AI` -> `{TELEGRAM_WEBAPP_URL}/ai`
- `Дедлайны` -> `{TELEGRAM_WEBAPP_URL}/deadlines`
- `Premium` -> `{TELEGRAM_WEBAPP_URL}/pricing`

## Telegram Stars

For digital access inside Telegram, use Stars as the primary method.

Bot commands:

```text
/premium
/buy
/payments
/restore
/support
```

The bot sends invoices with:

```text
currency=XTR
provider_token=""
payload=<internal order id>
```

Access is activated only after Telegram sends `successful_payment` and the API confirms the order.

## Webhook checks

1. Open bot health:

```text
https://ENT_GRANT_BOT_DOMAIN/health
```

Expected:

```json
{ "status": "ok", "service": "bot" }
```

2. Check webhook from a terminal with env loaded:

```bash
bash scripts/get_telegram_webhook_info.sh
```

The `url` should equal:

```text
https://ENT_GRANT_BOT_DOMAIN/webhook
```

3. Open Telegram and send `/start` to `@entgrant_kz_bot`.

## Manual scripts

Run these only from a local shell or Railway shell with environment variables loaded:

```bash
bash scripts/check_telegram_env.sh
bash scripts/set_telegram_webhook.sh
bash scripts/set_telegram_menu_button.sh
bash scripts/set_telegram_commands.sh
bash scripts/get_telegram_webhook_info.sh
```

To remove webhook:

```bash
bash scripts/delete_telegram_webhook.sh
```

Scripts never print the full bot token.
