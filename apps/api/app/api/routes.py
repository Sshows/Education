from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import EducationProgram, ProgramGroup, SourceDocument, University, User
from app.schemas.common import (
    AIChatRequest,
    AIChatResponse,
    ForecastRequest,
    ForecastResponse,
    ProgramGroupResponse,
    SourceDocumentResponse,
    UniversityResponse,
)
from app.services.forecast_service import ForecastService
from app.services.ingestion_service import fetch_source, parse_source
from app.utils.telegram import validate_telegram_init_data

router = APIRouter(prefix="/api")


@router.get("/health")
def api_health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@router.post("/auth/telegram")
def auth_telegram(payload: dict, db: Session = Depends(get_db)):
    init_data = payload.get("initData", "")
    if settings.environment != "development" and not validate_telegram_init_data(init_data, settings.telegram_bot_token):
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    tg = payload.get("telegram", {})
    tg_id = tg.get("id", 0)
    user = db.scalar(select(User).where(User.telegram_id == tg_id))
    if not user:
        user = User(telegram_id=tg_id)
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
        grant_status=res.grant_status,
        confidence=res.confidence,
        error_margin_pp=res.error_margin_pp,
        explanation=res.explanation,
        sources=res.sources,
    )


@router.post("/forecast/bulk")
def forecast_bulk(payload: dict):
    return {"items": [], "message": "MVP: bulk ranking endpoint is ready for extension"}


@router.get("/universities", response_model=list[UniversityResponse])
def list_universities(db: Session = Depends(get_db)):
    return db.scalars(select(University)).all()


@router.get("/universities/{university_id}", response_model=UniversityResponse)
def get_university(university_id: int, db: Session = Depends(get_db)):
    u = db.scalar(select(University).where(University.id == university_id))
    if not u:
        raise HTTPException(404, "University not found")
    return u


@router.get("/universities/{university_id}/programs")
def list_university_programs(university_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(EducationProgram).where(EducationProgram.university_id == university_id)).all()


@router.get("/program-groups", response_model=list[ProgramGroupResponse])
def list_program_groups(db: Session = Depends(get_db)):
    return db.scalars(select(ProgramGroup)).all()


@router.get("/program-groups/{code}", response_model=ProgramGroupResponse)
def get_program_group(code: str, db: Session = Depends(get_db)):
    pg = db.scalar(select(ProgramGroup).where(ProgramGroup.code == code))
    if not pg:
        raise HTTPException(404, "Program group not found")
    return pg


@router.get("/sources", response_model=list[SourceDocumentResponse])
def list_sources(db: Session = Depends(get_db)):
    return db.scalars(select(SourceDocument)).all()


@router.get("/sources/{source_id}", response_model=SourceDocumentResponse)
def get_source(source_id: int, db: Session = Depends(get_db)):
    src = db.scalar(select(SourceDocument).where(SourceDocument.id == source_id))
    if not src:
        raise HTTPException(404, "Source not found")
    return src


@router.post("/ai/chat", response_model=AIChatResponse)
def ai_chat(payload: AIChatRequest, db: Session = Depends(get_db)):
    sources = db.scalars(select(SourceDocument).where(SourceDocument.status == "parsed").order_by(SourceDocument.priority).limit(3)).all()
    source_payload = [{"url": s.url, "publisher": s.publisher, "fetched_at": s.fetched_at} for s in sources]
    if not settings.openai_api_key:
        answer = "AI-консультант пока не подключён. Но по имеющимся данным: используйте калькулятор как ориентир и проверяйте официальные источники. Гарантия поступления невозможна."
        if not sources:
            answer = "Подтверждённых данных в источниках нет."
        return AIChatResponse(answer=answer, sources=source_payload, updated_at=datetime.utcnow())

    # Safe placeholder for external LLM integration.
    if not sources:
        return AIChatResponse(answer="Подтверждённых данных в источниках нет.", sources=[], updated_at=datetime.utcnow())
    return AIChatResponse(
        answer="Ответ сформирован по подтверждённым источникам. Всегда проверяйте официальные страницы НЦТ/МНВО. Поступление не гарантируется.",
        sources=source_payload,
        updated_at=datetime.utcnow(),
    )


@router.get("/ai/history")
def ai_history():
    return {"items": []}




@router.post("/admin/sources")
def admin_create_source(payload: dict, db: Session = Depends(get_db)):
    required = ["title", "url", "source_type", "publisher", "priority"]
    for key in required:
        if key not in payload:
            raise HTTPException(400, f"Missing field: {key}")
    src = SourceDocument(
        title=payload["title"],
        url=payload["url"],
        source_type=payload["source_type"],
        publisher=payload["publisher"],
        priority=int(payload["priority"]),
        status="pending",
    )
    db.add(src)
    db.commit()
    db.refresh(src)
    return src


@router.get("/admin/sources", response_model=list[SourceDocumentResponse])
def admin_list_sources(db: Session = Depends(get_db)):
    return db.scalars(select(SourceDocument)).all()


@router.post("/admin/sources/{source_id}/fetch")
def admin_fetch_source(source_id: int, db: Session = Depends(get_db)):
    src = fetch_source(db, source_id)
    return {"source_id": source_id, "status": src.status, "fetched_at": src.fetched_at}


@router.post("/admin/sources/{source_id}/parse")
def admin_parse_source(source_id: int, db: Session = Depends(get_db)):
    src = parse_source(db, source_id)
    return {"source_id": source_id, "status": src.status, "error_message": src.error_message}


@router.get("/admin/conflicts")
def admin_conflicts(db: Session = Depends(get_db)):
    from app.models.models import AdmissionThreshold

    items = db.scalars(select(AdmissionThreshold).where(AdmissionThreshold.is_conflict.is_(True))).all()
    return {"items": [{"id": x.id, "year": x.year, "message": "Есть расхождение в источниках"} for x in items]}


@router.post("/admin/import/csv")
def admin_import_csv():
    return {"status": "queued"}
