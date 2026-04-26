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
require_env TELEGRAM_WEBHOOK_URL
require_env TELEGRAM_WEBHOOK_SECRET

echo "Setting Telegram webhook for ${TELEGRAM_WEBHOOK_URL}"
curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${TELEGRAM_WEBHOOK_URL}" \
  -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}" \
  -d "drop_pending_updates=true" \
  -d 'allowed_updates=["message","callback_query"]'
echo
