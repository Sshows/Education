#!/usr/bin/env bash
set -euo pipefail

require_env() {
  local name="$1"
  if [ -z "${!name:-}" ]; then
    echo "Missing required env: ${name}" >&2
    exit 1
  fi
}

require_env TELEGRAM_BOT_TOKEN
require_env TELEGRAM_WEBAPP_URL

echo "Setting Telegram menu button for ${TELEGRAM_WEBAPP_URL}"
curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setChatMenuButton" \
  -H "Content-Type: application/json" \
  -d "{\"menu_button\":{\"type\":\"web_app\",\"text\":\"ENT Grant\",\"web_app\":{\"url\":\"${TELEGRAM_WEBAPP_URL}\"}}}"
echo
