#!/usr/bin/env bash
set -euo pipefail

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "Missing required env: TELEGRAM_BOT_TOKEN" >&2
  exit 1
fi

echo "Setting Telegram bot commands"
curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setMyCommands" \
  -H "Content-Type: application/json" \
  -d '{"commands":[{"command":"start","description":"Запустить бота"},{"command":"calc","description":"Рассчитать шанс"},{"command":"programs","description":"Программы"},{"command":"universities","description":"Вузы"},{"command":"deadlines","description":"Дедлайны"},{"command":"profile","description":"Профиль"},{"command":"ask","description":"AI-консультант"},{"command":"sources","description":"Источники"},{"command":"help","description":"Помощь"}]}'
echo
