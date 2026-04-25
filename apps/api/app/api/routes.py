from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import ProgramGroup, SourceDocument, University, User
from app.schemas.forecast import ForecastRequest, ForecastResponse
from app.services.forecast_service import ForecastService
from app.utils.telegram import validate_telegram_init_data

router = APIRouter(prefix="/api")


@router.post("/auth/telegram")
def auth_telegram(payload: dict, db: Session = Depends(get_db)):
    init_data = payload.get("initData", "")
    if not validate_telegram_init_data(init_data, settings.telegram_bot_token):
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    tg = payload.get("telegram", {})
    user = db.scalar(select(User).where(User.telegram_id == tg.get("id")))
    if not user:
        user = User(telegram_id=tg["id"])
        db.add(user)
    user.first_name = tg.get("first_name")
    user.last_name = tg.get("last_name")
    user.username = tg.get("username")
    user.language_code = tg.get("language_code")
    db.commit()
    return {"token": "session-token-placeholder", "user_id": user.id}




@router.get("/profile")
def get_profile():
    return {"profile": None}


@router.put("/profile")
def put_profile(payload: dict):
    return {"profile": payload}
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
def ai_chat(payload: dict):
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
