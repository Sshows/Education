#!/usr/bin/env bash
set -euo pipefail

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "Missing required env: TELEGRAM_BOT_TOKEN" >&2
  exit 1
fi

curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"
echo
