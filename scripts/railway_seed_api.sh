#!/usr/bin/env bash
set -euo pipefail

if ! command -v railway >/dev/null 2>&1; then
  echo "railway CLI is not installed"
  exit 1
fi

railway run python -m app.scripts.seed_sources
