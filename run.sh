#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
URL="file://$SCRIPT_DIR/index.html"

if command -v chromium >/dev/null 2>&1; then
  BROWSER="chromium"
elif command -v chromium-browser >/dev/null 2>&1; then
  BROWSER="chromium-browser"
elif command -v google-chrome >/dev/null 2>&1; then
  BROWSER="google-chrome"
else
  echo "Не найден Chromium/Chrome."
  echo "Установи браузер, например:"
  echo "  sudo apt install chromium"
  exit 1
fi

exec "$BROWSER" \
  --kiosk \
  --start-fullscreen \
  --autoplay-policy=no-user-gesture-required \
  "$URL"