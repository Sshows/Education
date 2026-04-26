from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import models  # noqa: F401


def make_client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
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


def test_product_list_returns_active_products():
    client = make_client()

    response = client.get("/api/payments/products")

    app.dependency_overrides.clear()
    assert response.status_code == 200
    codes = {item["code"] for item in response.json()}
    assert {"free", "pro_once", "ai_pack", "premium_month"} <= codes


def test_create_telegram_stars_order():
    client = make_client()

    response = client.post(
        "/api/payments/telegram-stars/order",
        json={"product_code": "pro_once", "telegram_id": 1001, "idempotency_key": "order-1"},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    body = response.json()
    assert body["provider"] == "telegram_stars"
    assert body["currency"] == "XTR"
    assert body["amount"] == 50
    assert body["telegram_invoice_payload"] == str(body["order_id"])


def test_idempotent_order_creation():
    client = make_client()
    payload = {"product_code": "premium_month", "telegram_id": 1002, "idempotency_key": "same-order"}

    first = client.post("/api/payments/telegram-stars/order", json=payload)
    second = client.post("/api/payments/telegram-stars/order", json=payload)

    app.dependency_overrides.clear()
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["order_id"] == second.json()["order_id"]


def test_cannot_mark_paid_with_wrong_amount():
    client = make_client()
    order = client.post(
        "/api/payments/telegram-stars/order",
        json={"product_code": "pro_once", "telegram_id": 1003, "idempotency_key": "wrong-amount"},
    ).json()

    response = client.post(
        "/api/payments/telegram-stars/confirm",
        json={
            "order_id": order["order_id"],
            "telegram_id": 1003,
            "total_amount": 49,
            "currency": "XTR",
            "telegram_payment_charge_id": "tg-charge-wrong",
        },
    )

    app.dependency_overrides.clear()
    assert response.status_code == 400


def test_successful_payment_grants_entitlement_and_duplicate_confirm_does_not_duplicate_entitlement():
    client = make_client()
    order = client.post(
        "/api/payments/telegram-stars/order",
        json={"product_code": "ai_pack", "telegram_id": 1004, "idempotency_key": "paid-once"},
    ).json()
    confirm = {
        "order_id": order["order_id"],
        "telegram_id": 1004,
        "total_amount": 100,
        "currency": "XTR",
        "telegram_payment_charge_id": "tg-charge-1",
    }

    first = client.post("/api/payments/telegram-stars/confirm", json=confirm)
    second = client.post("/api/payments/telegram-stars/confirm", json={**confirm, "telegram_payment_charge_id": "tg-charge-2"})
    entitlements = client.get("/api/payments/my-entitlements", params={"telegram_id": 1004})

    app.dependency_overrides.clear()
    assert first.status_code == 200
    assert second.status_code == 200
    assert entitlements.status_code == 200
    assert len(entitlements.json()) == 1
    assert entitlements.json()[0]["product_code"] == "ai_pack"


def test_entitlement_check_and_ai_credit_consumption():
    client = make_client()
    order = client.post(
        "/api/payments/telegram-stars/order",
        json={"product_code": "ai_pack", "telegram_id": 1005, "idempotency_key": "credits"},
    ).json()
    client.post(
        "/api/payments/telegram-stars/confirm",
        json={
            "order_id": order["order_id"],
            "telegram_id": 1005,
            "total_amount": 100,
            "currency": "XTR",
            "telegram_payment_charge_id": "tg-charge-credits",
        },
    )

    consume = client.post("/api/payments/consume-credit", json={"telegram_id": 1005, "feature": "ai_questions"})

    app.dependency_overrides.clear()
    assert consume.status_code == 200
    assert consume.json()["credits_used"] == 1


def test_disabled_provider_returns_safe_error():
    client = make_client()

    response = client.post(
        "/api/payments/orders",
        json={"product_code": "premium_month", "provider": "kaspi", "telegram_id": 1006},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 400
    assert "Kaspi" in response.json()["detail"]


def test_external_provider_without_credentials_returns_safe_error(monkeypatch):
    monkeypatch.setattr(settings, "payments_enable_freedom", True)
    monkeypatch.setattr(settings, "freedom_pay_enabled", True)
    monkeypatch.setattr(settings, "freedom_pay_merchant_id", "")
    monkeypatch.setattr(settings, "freedom_pay_secret_key", "")
    client = make_client()

    response = client.post(
        "/api/payments/orders",
        json={"product_code": "premium_month", "provider": "freedom_pay", "telegram_id": 1007},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 400
    assert "credentials" in response.json()["detail"]
