from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.ent_subjects import (
    SUBJECT_COMBINATIONS,
    get_combination_by_alias,
    get_combination_by_pair,
    get_recommended_codes_for_pair,
    normalize_alias_to_subjects,
    subject_pair_key,
)
from app.models.models import Analysis, HistoricalCutoff, ProgramGroup, User
from app.services.payments.service import PaymentService


SUBJECT_ALIASES: dict[str, tuple[str, str]] = {
    "math_cs": ("mathematics", "informatics"),
    "informatics_math": ("mathematics", "informatics"),
    "math_physics": ("mathematics", "physics"),
    "physics_math": ("mathematics", "physics"),
    "math_geo": ("mathematics", "geography"),
    "bio_chem": ("biology", "chemistry"),
    "chem_bio": ("biology", "chemistry"),
    "bio_geo": ("biology", "geography"),
    "history_law": ("world_history", "fundamentals_of_law"),
    "history_geo": ("world_history", "geography"),
}


DEMO_SPECIALTIES: list[dict[str, Any]] = [
    {"code": "B057", "name": "Информационные технологии", "subject_pair": "informatics+mathematics", "base": 88, "count": 1460},
    {"code": "B058", "name": "Информационная безопасность", "subject_pair": "informatics+mathematics", "base": 92, "count": 680},
    {"code": "B059", "name": "Коммуникации и коммуникационные технологии", "subject_pair": "informatics+mathematics", "base": 80, "count": 820},
    {"code": "B157", "name": "Информационные системы и технологии", "subject_pair": "informatics+mathematics", "base": 84, "count": 520},
    {"code": "B044", "name": "Менеджмент и управление", "subject_pair": "geography+mathematics", "base": 73, "count": 900},
    {"code": "B045", "name": "Аудит и налогообложение", "subject_pair": "geography+mathematics", "base": 70, "count": 740},
    {"code": "B046", "name": "Финансы, экономика и банковское дело", "subject_pair": "geography+mathematics", "base": 76, "count": 880},
    {"code": "B049", "name": "Право", "subject_pair": "fundamentals_of_law+world_history", "base": 84, "count": 620},
    {"code": "B085", "name": "Медицина", "subject_pair": "biology+chemistry", "base": 101, "count": 1600},
    {"code": "B084", "name": "Сестринское дело", "subject_pair": "biology+chemistry", "base": 78, "count": 500},
    {"code": "B086", "name": "Фармация", "subject_pair": "biology+chemistry", "base": 91, "count": 420},
    {"code": "B071", "name": "Горное дело и добыча полезных ископаемых", "subject_pair": "mathematics+physics", "base": 74, "count": 760},
    {"code": "B074", "name": "Градостроительство, строительные работы", "subject_pair": "mathematics+physics", "base": 72, "count": 840},
    {"code": "B036", "name": "Переводческое дело", "subject_pair": "foreign_language+world_history", "base": 82, "count": 360},
    {"code": "B001", "name": "Педагогика и психология", "subject_pair": "biology+geography", "base": 68, "count": 980},
]


@dataclass
class HistoricalScore:
    year: int
    min_score: int
    grants_count: int | None = None


def _demo_history(base: int, quota: str) -> list[HistoricalScore]:
    adjustment = -10 if quota in {"rural", "village", "quota"} else 0
    years = range(2017, 2026)
    return [
        HistoricalScore(year=year, min_score=max(50, base + (year - 2017) * 2 + adjustment), grants_count=100 + (year - 2017) * 5)
        for year in years
    ]


def weighted_historical(scores: list[HistoricalScore], user_score: int) -> float:
    total_weight = 0.0
    weighted_pass = 0.0
    for idx, score in enumerate(sorted(scores, key=lambda item: item.year)):
        weight = float(idx + 1)
        if score.year in {2020, 2021}:
            weight *= 0.6
        total_weight += weight
        if user_score >= score.min_score:
            weighted_pass += weight
    return weighted_pass / total_weight if total_weight else 0.0


def predict_next_cutoff(scores: list[HistoricalScore], grants_delta: int = 0) -> int:
    recent = sorted(scores, key=lambda item: item.year)[-3:]
    if len(recent) < 3:
        return recent[-1].min_score if recent else 0
    predicted = recent[-3].min_score * 0.20 + recent[-2].min_score * 0.35 + recent[-1].min_score * 0.45
    if grants_delta < 0:
        predicted += abs(grants_delta) * 0.15
    return round(predicted)


def chance_for_scores(scores: list[HistoricalScore], user_score: int) -> tuple[int, int, int, str]:
    hist = weighted_historical(scores, user_score)
    grants_delta = 0
    if len(scores) >= 2 and scores[-1].grants_count is not None and scores[-2].grants_count is not None:
        grants_delta = int(scores[-1].grants_count or 0) - int(scores[-2].grants_count or 0)
    predicted = predict_next_cutoff(scores, grants_delta)
    gap = user_score - predicted
    if gap >= 15:
        trend = 0.92
    elif gap >= 5:
        trend = 0.78
    elif gap >= 0:
        trend = 0.60
    elif gap >= -10:
        trend = 0.32
    else:
        trend = 0.08

    values = [item.min_score for item in scores]
    volatility = max(values) - min(values) if values else 0
    stability = 0.05 if volatility < 10 else -0.05 if volatility > 20 else 0
    final = hist * 0.40 + trend * 0.40 + stability + (0.20 if gap > 0 else 0)
    chance = min(97, max(3, round(final * 100)))
    trend_label = "growing" if len(values) >= 2 and values[-1] > values[0] else "stable"
    return chance, predicted, gap, trend_label


class AnalysisService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def normalize_subject_pair_key(self, raw: str) -> str:
        raw = (raw or "").strip()
        if not raw:
            return subject_pair_key("mathematics", "informatics")
        if "+" in raw:
            first, second = raw.split("+", 1)
            combo = get_combination_by_pair(first.strip(), second.strip())
            if combo:
                return combo.key
        alias_pair = SUBJECT_ALIASES.get(raw.lower()) or normalize_alias_to_subjects(raw)
        if alias_pair:
            return subject_pair_key(alias_pair[0], alias_pair[1])
        combo = get_combination_by_alias(raw)
        if combo:
            return combo.key
        return raw

    def list_specialties(self, subject: str | None = None) -> list[dict[str, Any]]:
        pair_key = self.normalize_subject_pair_key(subject or "") if subject else None
        db_programs = self.db.scalars(select(ProgramGroup)).all()
        items: list[dict[str, Any]] = []
        for program in db_programs:
            program_pair = subject_pair_key(program.profile_subject_1, program.profile_subject_2)
            if pair_key and program_pair != pair_key:
                continue
            items.append({"code": program.code, "name": program.name_ru, "subject_pair": program_pair})
        if items:
            return items
        return [
            {"code": item["code"], "name": item["name"], "subject_pair": item["subject_pair"]}
            for item in DEMO_SPECIALTIES
            if pair_key is None or item["subject_pair"] == pair_key
        ]

    def _history_for_spec(self, spec_code: str, quota: str) -> list[HistoricalScore]:
        program = self.db.scalar(select(ProgramGroup).where(ProgramGroup.code == spec_code))
        if program:
            rows = self.db.scalars(
                select(HistoricalCutoff)
                .where(HistoricalCutoff.program_group_id == program.id)
                .order_by(HistoricalCutoff.year)
            ).all()
            if rows:
                return [HistoricalScore(year=row.year, min_score=row.min_score, grants_count=row.grants_count) for row in rows]
        demo = next((item for item in DEMO_SPECIALTIES if item["code"] == spec_code), None)
        return _demo_history(int(demo["base"]) if demo else 80, quota)

    def _spec_name(self, spec_code: str) -> str:
        program = self.db.scalar(select(ProgramGroup).where(ProgramGroup.code == spec_code))
        if program:
            return program.name_ru
        demo = next((item for item in DEMO_SPECIALTIES if item["code"] == spec_code), None)
        return str(demo["name"]) if demo else spec_code

    def _user_access(self, tg_id: int | None) -> tuple[User | None, bool, bool]:
        if tg_id is None:
            return None, True, False
        user = self.db.scalar(select(User).where(User.telegram_id == tg_id))
        if not user:
            user = User(telegram_id=tg_id, free_analysis_used=False)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        has_paid_access = PaymentService(self.db).has_entitlement(tg_id, {"pro_once", "premium_month"})
        first_free = not user.free_analysis_used
        return user, first_free or has_paid_access, has_paid_access

    def analyze(self, payload: dict[str, Any]) -> dict[str, Any]:
        tg_id = payload.get("tg_id") or payload.get("telegram_id")
        tg_id = int(tg_id) if tg_id is not None else None
        score = int(payload.get("score", 0))
        quota = str(payload.get("quota") or "general")
        pair_key = self.normalize_subject_pair_key(str(payload.get("subject_pair") or payload.get("combo") or "math_cs"))

        pair_parts = pair_key.split("+", 1)
        spec_codes = payload.get("spec_codes") or (
            get_recommended_codes_for_pair(pair_parts[0], pair_parts[1]) if len(pair_parts) == 2 else []
        )
        if not spec_codes:
            spec_codes = [item["code"] for item in self.list_specialties(pair_key)[:4]]
        spec_codes = [str(code).upper() for code in spec_codes][:8]

        user, is_free, has_paid_access = self._user_access(tg_id)
        results = []
        for spec_code in spec_codes:
            scores = self._history_for_spec(spec_code, quota)
            chance, predicted, gap, trend = chance_for_scores(scores, score)
            results.append(
                {
                    "spec_code": spec_code,
                    "name": self._spec_name(spec_code),
                    "chance": chance,
                    "predicted_2025": predicted,
                    "gap": gap,
                    "trend": trend,
                    "history": [{"year": item.year, "min": item.min_score} for item in scores],
                }
            )

        recommendations = sorted(results, key=lambda item: item["chance"], reverse=True)[:3]
        response = {
            "is_free": is_free,
            "has_paid_access": has_paid_access,
            "paywall": not is_free,
            "subject_pair": pair_key,
            "score": score,
            "quota": quota,
            "results": results,
            "recommendations": recommendations,
            "card_status": "queued" if is_free else "locked_until_payment",
            "share_text": "Проверил шансы на грант — попробуй и ты",
        }

        analysis = Analysis(
            user_id=user.id if user else None,
            telegram_id=tg_id,
            score=score,
            subject_pair=pair_key,
            quota=quota,
            specs_json=spec_codes,
            result_json=response,
            card_url=None,
            created_at=datetime.utcnow(),
        )
        self.db.add(analysis)
        if user and is_free and not has_paid_access and not user.free_analysis_used:
            user.free_analysis_used = True
        self.db.commit()
        self.db.refresh(analysis)
        response["analysis_id"] = analysis.id
        return response
