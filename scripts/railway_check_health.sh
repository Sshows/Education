#!/usr/bin/env bash
set -euo pipefail

: "${API_URL:?API_URL is required}"
: "${WEB_URL:?WEB_URL is required}"

curl -fsS "${API_URL}/health"
curl -fsS "${API_URL}/docs" >/dev/null
curl -fsS "${WEB_URL}" >/dev/null

echo "Health checks passed"
