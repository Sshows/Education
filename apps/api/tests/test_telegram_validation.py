import hashlib
import hmac
import json
from urllib.parse import urlencode

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.routes import router
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import models  # noqa: F401
from app.utils.telegram import validate_telegram_init_data


def make_init_data(bot_token: str, user: dict) -> str:
    pairs = {
        "auth_date": "1710000000",
        "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
        "user": json.dumps(user, separators=(",", ":")),
    }
    data_check_string = "\n".join(f"{key}={value}" for key, value in sorted(pairs.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    pairs["hash"] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return urlencode(pairs)


def make_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


def test_valid_init_data_is_accepted(monkeypatch):
    monkeypatch.setattr(settings, "telegram_bot_token", "123456:test-token")
    monkeypatch.setattr(settings, "telegram_auth_bot_token", "")
    monkeypatch.setattr(settings, "environment", "production")
    client = make_client()

    init_data = make_init_data(
        "123456:test-token",
        {"id": 42, "first_name": "Ayan", "username": "ayan"},
    )

    response = client.post("/api/auth/telegram", json={"initData": init_data})

    app.dependency_overrides.clear()
    assert response.status_code == 200
    body = response.json()
    assert body["auth_method"] == "telegram"
    assert body["user"]["telegram_id"] == 42
    assert body["token"].startswith("tg_")


def test_invalid_init_data_rejected():
    assert not validate_telegram_init_data("user=%7B%7D", "token")


def test_invalid_production_auth_rejected(monkeypatch):
    monkeypatch.setattr(settings, "telegram_bot_token", "123456:test-token")
    monkeypatch.setattr(settings, "telegram_auth_bot_token", "")
    monkeypatch.setattr(settings, "environment", "production")
    client = make_client()

    response = client.post("/api/auth/telegram", json={"initData": "user=%7B%7D&hash=bad"})

    app.dependency_overrides.clear()
    assert response.status_code == 401


def test_missing_init_data_production_rejected(monkeypatch):
    monkeypatch.setattr(settings, "environment", "production")
    client = make_client()

    response = client.post("/api/auth/telegram", json={})

    app.dependency_overrides.clear()
    assert response.status_code == 401


def test_development_fallback_allowed(monkeypatch):
    monkeypatch.setattr(settings, "environment", "development")
    client = make_client()

    response = client.post("/api/auth/telegram", json={})

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["auth_method"] == "development"
