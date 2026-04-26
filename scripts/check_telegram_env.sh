#!/usr/bin/env bash
set -euo pipefail

mask_token() {
  local token="$1"
  local prefix="${token:0:6}"
  local suffix="${token: -4}"
  echo "${prefix}...${suffix}"
}

check_env() {
  local name="$1"
  if [ -z "${!name:-}" ]; then
    echo "missing ${name}"
    return 1
  fi
  echo "ok ${name}"
}

status=0
check_env TELEGRAM_BOT_TOKEN || status=1
check_env TELEGRAM_WEBAPP_URL || status=1
check_env TELEGRAM_WEBHOOK_URL || status=1
check_env TELEGRAM_WEBHOOK_SECRET || status=1

echo "TELEGRAM_AUTO_SET_WEBHOOK=${TELEGRAM_AUTO_SET_WEBHOOK:-false}"
echo "TELEGRAM_AUTO_SET_MENU_BUTTON=${TELEGRAM_AUTO_SET_MENU_BUTTON:-true}"
echo "TELEGRAM_AUTO_SET_COMMANDS=${TELEGRAM_AUTO_SET_COMMANDS:-true}"

if [ -n "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "TELEGRAM_BOT_TOKEN=$(mask_token "${TELEGRAM_BOT_TOKEN}")"
fi

exit "${status}"
