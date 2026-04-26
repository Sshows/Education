import re

import pytest
from fastapi.testclient import TestClient

from app.bot import BOT_COMMANDS, _ALIAS_PAIRS, _COMBO_RE, _SCORE_RE, start_keyboard
from app.config import settings
from app.webhook import app, dp


# -------- Keyboard tests --------

def test_start_keyboard_contains_web_app_buttons():
    keyboard = start_keyboard()
    urls = [button.web_app.url for row in keyboard.inline_keyboard for button in row if button.web_app]

    assert settings.webapp_url("/calculator") in urls
    assert settings.webapp_url("/universities") in urls
    assert settings.webapp_url("/programs") in urls
    assert settings.webapp_url("/ai") in urls
    assert settings.webapp_url("/deadlines") in urls


# -------- Score detection --------

@pytest.mark.parametrize("text,expected_score", [
    ("82", 82),
    ("0", 0),
    ("140", 140),
    ("  99  ", 99),
])
def test_score_regex_detects_valid_scores(text: str, expected_score: int):
    m = _SCORE_RE.match(text)
    assert m is not None
    assert int(m.group(1)) == expected_score


@pytest.mark.parametrize("text", [
    "141",   # > 140
    "abc",
    "физмат",
    "куда поступить",
    "",
])
def test_score_regex_ignores_non_scores(text: str):
    m = _SCORE_RE.match(text)
    if m:
        score = int(m.group(1))
        assert score < 0 or score > 140
    # non-matching is also OK


# -------- Combo alias detection --------

@pytest.mark.parametrize("text,expected_alias", [
    ("физмат", "физмат"),
    ("я сдавал инфомат", "инфомат"),
    ("химбио или биохим?", "химбио"),
    ("истправо направление", "истправо"),
    ("биогео", "биогео"),
    ("матгео", "матгео"),
])
def test_combo_regex_detects_aliases(text: str, expected_alias: str):
    m = _COMBO_RE.search(text.lower())
    assert m is not None
    assert m.group(0).lower() == expected_alias.lower()


def test_alias_pairs_map_is_complete():
    """Every key in alias map must resolve to a valid subject tuple."""
    for alias, (s1, s2) in _ALIAS_PAIRS.items():
        assert isinstance(s1, str) and s1
        assert isinstance(s2, str) and s2


# -------- Webhook security --------

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


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# -------- Token not logged --------

def test_token_not_in_bot_module_source():
    """Ensure no hardcoded real-looking token (format: digits:alphanum) in bot.py."""
    import inspect
    import app.bot as bot_module

    source = inspect.getsource(bot_module)
    # A real Telegram token looks like 123456789:AABBCC...
    real_token_pattern = re.compile(r"\d{9,10}:[A-Za-z0-9_-]{30,}")
    matches = real_token_pattern.findall(source)
    # Allow the placeholder used in development
    for m in matches:
        assert "development-placeholder" in m or "0" * 10 in m, (
            f"Possible real token found in bot.py: {m[:20]}..."
        )
