from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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


def test_specialties_endpoint_supports_customer_subject_alias():
    client = make_client()

    response = client.get("/api/specialties", params={"subject": "math_cs"})

    app.dependency_overrides.clear()
    assert response.status_code == 200
    codes = {item["code"] for item in response.json()}
    assert {"B057", "B058", "B059"} <= codes


def test_analyze_first_free_then_paywall_preview():
    client = make_client()
    payload = {
        "tg_id": 424242,
        "score": 110,
        "subject_pair": "math_cs",
        "quota": "general",
        "spec_codes": ["B057", "B058"],
    }

    first = client.post("/api/analyze", json=payload)
    second = client.post("/api/analyze", json=payload)

    app.dependency_overrides.clear()
    assert first.status_code == 200
    assert first.json()["is_free"] is True
    assert first.json()["results"][0]["spec_code"] == "B057"
    assert first.json()["results"][0]["chance"] >= 3
    assert second.status_code == 200
    assert second.json()["is_free"] is False
    assert second.json()["paywall"] is True


def test_legacy_aipay_create_is_safe_when_disabled():
    client = make_client()

    response = client.post(
        "/api/payment/create",
        json={"tg_id": 1, "product_code": "pro_once", "provider": "aipay"},
    )

    app.dependency_overrides.clear()
    assert response.status_code == 400
    assert "AiPay" in response.json()["detail"]
