import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import ProgramGroup, SourceDocument, University, User
from app.schemas.forecast import ForecastRequest, ForecastResponse
from app.services.forecast_service import ForecastService
from app.utils.telegram import parse_telegram_user, validate_telegram_init_data

router = APIRouter(prefix="/api")


@router.post("/auth/telegram")
def auth_telegram(payload: dict, db: Session = Depends(get_db)):
    init_data = payload.get("initData", "")
    if init_data:
        if not validate_telegram_init_data(init_data, settings.telegram_initdata_token):
            raise HTTPException(status_code=401, detail="Invalid Telegram initData")
        tg = parse_telegram_user(init_data)
        auth_method = "telegram"
    elif settings.environment == "development":
        tg = payload.get("telegram") or {"id": 1, "first_name": "Dev", "language_code": "ru"}
        auth_method = "development"
    else:
        raise HTTPException(status_code=401, detail="Telegram initData is required")

    telegram_id = tg.get("id")
    if not telegram_id:
        raise HTTPException(status_code=401, detail="Telegram user is missing")

    user = db.scalar(select(User).where(User.telegram_id == tg.get("id")))
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
    user.first_name = tg.get("first_name")
    user.last_name = tg.get("last_name")
    user.username = tg.get("username")
    user.language_code = tg.get("language_code")
    db.commit()
    db.refresh(user)

    token = hmac.new(
        settings.session_secret.encode(),
        f"{user.telegram_id}:{user.id}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return {
        "token": f"tg_{token}",
        "auth_method": auth_method,
        "user": {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "language_code": user.language_code,
        },
    }


@router.get("/profile")
def get_profile():
    return {"profile": None}


@router.put("/profile")
def put_profile(payload: dict):
    return {"profile": payload}


@router.get("/bot/profile")
def bot_profile():
    return {
        "name": "ENT Grant",
        "commands": ["/start", "/calc", "/programs", "/universities", "/deadlines", "/profile", "/ask", "/sources", "/help"],
    }


@router.get("/analytics/summary")
def analytics_summary():
    return {
        "forecasts_total": 0,
        "active_users_7d": 0,
        "top_programs": [],
        "source_status": "demo",
    }


@router.post("/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest, db: Session = Depends(get_db)):
    res = ForecastService(db).calculate(req.profile, req.university_id, req.program_group_id)
    return ForecastResponse(
        grant_probability=res.grant_probability,
        paid_status=res.paid_status,
        confidence=res.confidence,
        error_margin_pp=res.error_margin_pp,
        explanation=res.explanation,
        source_ids=res.source_ids,
        status=res.status,
    )


@router.post("/forecast/bulk")
def forecast_bulk(payload: dict):
    return {"items": [], "message": "MVP stub: bulk ranking to be expanded"}


@router.get("/universities")
def list_universities(db: Session = Depends(get_db)):
    return db.scalars(select(University)).all()


@router.get("/universities/{university_id}")
def get_university(university_id: int, db: Session = Depends(get_db)):
    u = db.scalar(select(University).where(University.id == university_id))
    if not u:
        raise HTTPException(404, "University not found")
    return u


@router.get("/program-groups")
def list_program_groups(db: Session = Depends(get_db)):
    return db.scalars(select(ProgramGroup)).all()


@router.get("/program-groups/{code}")
def get_program_group(code: str, db: Session = Depends(get_db)):
    pg = db.scalar(select(ProgramGroup).where(ProgramGroup.code == code))
    if not pg:
        raise HTTPException(404, "Program group not found")
    return pg


@router.get("/sources")
def list_sources(db: Session = Depends(get_db)):
    return db.scalars(select(SourceDocument)).all()


@router.get("/sources/{source_id}")
def get_source(source_id: int, db: Session = Depends(get_db)):
    src = db.scalar(select(SourceDocument).where(SourceDocument.id == source_id))
    if not src:
        raise HTTPException(404, "Source not found")
    return src


@router.post("/ai/chat")
def ai_chat(payload: dict, db: Session = Depends(get_db)):
    if payload.get("consume_credit"):
        from app.services.payments.errors import PaymentError
        from app.services.payments.service import PaymentService

        try:
            PaymentService(db).consume_credit(payload.get("telegram_id"), "ai_questions")
        except PaymentError as exc:
            raise HTTPException(status_code=exc.status_code, detail=str(exc))
    return {
        "answer": "Подтверждённых данных в источниках нет.",
        "sources": [],
        "updated_at": None,
    }


@router.get("/ai/history")
def ai_history():
    return {"items": []}


@router.post("/admin/sources")
def admin_create_source():
    return {"status": "ok"}


@router.post("/admin/sources/{source_id}/fetch")
def admin_fetch_source(source_id: int):
    return {"source_id": source_id, "status": "queued"}


@router.post("/admin/import/csv")
def admin_import_csv():
    return {"status": "queued"}


@router.get("/admin/conflicts")
def admin_conflicts():
    return {"items": [{"message": "Есть расхождение в источниках"}]}


@router.put("/admin/facts/{fact_id}/approve")
def admin_approve_fact(fact_id: int):
    return {"fact_id": fact_id, "status": "approved"}


@router.put("/admin/facts/{fact_id}/reject")
def admin_reject_fact(fact_id: int):
    return {"fact_id": fact_id, "status": "rejected"}
