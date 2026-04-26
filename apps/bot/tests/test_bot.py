from fastapi.testclient import TestClient

from app.bot import start_keyboard
from app.config import settings
from app.webhook import app, dp


def test_start_keyboard_contains_web_app_buttons():
    keyboard = start_keyboard()
    urls = [button.web_app.url for row in keyboard.inline_keyboard for button in row if button.web_app]

    assert settings.webapp_url("/calculator") in urls
    assert settings.webapp_url("/universities") in urls
    assert settings.webapp_url("/programs") in urls
    assert settings.webapp_url("/ai") in urls
    assert settings.webapp_url("/deadlines") in urls


def test_webhook_rejects_invalid_secret(monkeypatch):
    monkeypatch.setattr(settings, "telegram_webhook_secret", "expected-secret")
    client = TestClient(app)

    response = client.post("/webhook", json={"update_id": 1}, headers={"X-Telegram-Bot-Api-Secret-Token": "bad"})

    assert response.status_code == 403


def test_webhook_accepts_valid_secret(monkeypatch):
    async def fake_feed_update(*args, **kwargs):
        return None

    monkeypatch.setattr(settings, "telegram_webhook_secret", "expected-secret")
    monkeypatch.setattr(dp, "feed_update", fake_feed_update)
    client = TestClient(app)

    response = client.post(
        "/webhook",
        json={"update_id": 1},
        headers={"X-Telegram-Bot-Api-Secret-Token": "expected-secret"},
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}
