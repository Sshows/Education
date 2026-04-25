from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.models import (
    AdmissionThreshold,
    EntStatistics,
    GrantAllocation,
    HistoricalCutoff,
    ProgramGroup,
    SourceDocument,
)
from app.schemas.common import ApplicantProfileInput


@dataclass
class ForecastResult:
    grant_probability: int
    paid_status: str
    grant_status: str
    confidence: str
    error_margin_pp: int
    explanation: dict
    sources: list[dict]


class ForecastService:
    def __init__(self, db: Session):
        self.db = db

    def _validate_minimums(self, p: ApplicantProfileInput) -> None:
        if p.kazakhstan_history_score < 5:
            raise ValueError("History of Kazakhstan minimum is 5")
        if p.math_literacy_score < 3:
            raise ValueError("Math literacy minimum is 3")
        if p.reading_literacy_score < 3:
            raise ValueError("Reading literacy minimum is 3")
        if p.profile_subject_1_score < 5 or p.profile_subject_2_score < 5:
            raise ValueError("Each profile subject minimum is 5")

    def calculate(self, profile: ApplicantProfileInput, university_id: int, program_group_id: int) -> ForecastResult:
        self._validate_minimums(profile)

        pg = self.db.scalar(select(ProgramGroup).where(ProgramGroup.id == program_group_id))
        if not pg:
            raise ValueError("Program group not found")
        if (profile.profile_subject_1, profile.profile_subject_2) != (pg.profile_subject_1, pg.profile_subject_2):
            raise ValueError("Profile subjects mismatch with selected program group")

        thresholds = self.db.scalars(
            select(AdmissionThreshold).where(
                AdmissionThreshold.university_id == university_id,
                AdmissionThreshold.program_group_id == program_group_id,
            ).order_by(desc(AdmissionThreshold.year))
        ).all()

        if not thresholds:
            return ForecastResult(
                grant_probability=1,
                paid_status="unknown",
                grant_status="unknown",
                confidence="low",
                error_margin_pp=25,
                explanation={"threshold_check": "нет подтверждённых данных", "conflicts": []},
                sources=[],
            )

        latest_year = thresholds[0].year
        same_year_thresholds = [t for t in thresholds if t.year == latest_year]
        grant_values = {t.grant_min_score for t in same_year_thresholds if t.grant_min_score is not None}
        paid_values = {t.paid_min_score for t in same_year_thresholds if t.paid_min_score is not None}
        has_conflict = len(grant_values) > 1 or len(paid_values) > 1 or any(t.is_conflict for t in same_year_thresholds)

        strict_grant_threshold = max(grant_values) if grant_values else None
        paid_threshold = min(paid_values) if paid_values else None

        paid_eligible = paid_threshold is not None and profile.total_score >= paid_threshold
        grant_eligible = strict_grant_threshold is not None and profile.total_score >= strict_grant_threshold

        cutoffs = self.db.scalars(
            select(HistoricalCutoff).where(
                HistoricalCutoff.university_id == university_id,
                HistoricalCutoff.program_group_id == program_group_id,
                HistoricalCutoff.year >= 2020,
                HistoricalCutoff.year <= 2025,
            ).order_by(HistoricalCutoff.year)
        ).all()

        grants_now = self.db.scalar(select(GrantAllocation).where(GrantAllocation.program_group_id == program_group_id).order_by(desc(GrantAllocation.year)))
        grants_prev = self.db.scalar(
            select(GrantAllocation).where(
                GrantAllocation.program_group_id == program_group_id,
                GrantAllocation.year == (grants_now.year - 1 if grants_now else 2024),
            )
        )

        demand_now = self.db.scalar(select(EntStatistics).where(EntStatistics.subject_combo == profile.subject_combo).order_by(desc(EntStatistics.year)))
        demand_prev = self.db.scalar(
            select(EntStatistics).where(
                EntStatistics.subject_combo == profile.subject_combo,
                EntStatistics.year == (demand_now.year - 1 if demand_now else 2024),
            )
        )

        historical_scores = [c.min_score for c in cutoffs]
        weighted_cutoff = float(np.mean(historical_scores)) if historical_scores else float(strict_grant_threshold or profile.total_score)

        if len(historical_scores) >= 3:
            volatility = max(float(np.std(historical_scores)), 1.0)
        elif len(historical_scores) >= 1:
            volatility = 10.0
        else:
            volatility = 14.0

        confidence_reasons = []
        confidence = "high"

        if len(historical_scores) < 3:
            confidence = "medium"
            confidence_reasons.append("limited_historical_data")
        if len(historical_scores) == 0:
            confidence = "low"
            confidence_reasons.append("missing_historical_data")
        if not grants_now:
            confidence = "low"
            confidence_reasons.append("missing_grants")
        if not demand_now:
            confidence = "low"
            confidence_reasons.append("missing_demand")
        if has_conflict:
            confidence = "low" if confidence != "low" else confidence
            confidence_reasons.append("source_conflict")

        grant_supply_factor = 1.0
        if grants_now and grants_prev and grants_now.total_grants and grants_prev.total_grants:
            grant_supply_factor = grants_now.total_grants / max(grants_prev.total_grants, 1)
        else:
            confidence_reasons.append("supply_fallback_used")

        demand_factor = 1.0
        if demand_now and demand_prev and demand_now.participants_count and demand_prev.participants_count:
            demand_factor = demand_now.participants_count / max(demand_prev.participants_count, 1)
        else:
            confidence_reasons.append("demand_fallback_used")

        quota_factor = 0.0
        if profile.quota_category == "rural":
            quota_factor = 0.15 if grants_now and grants_now.quota_grants else 0.05
            if not (grants_now and grants_now.quota_grants):
                confidence = "low"
                confidence_reasons.append("rural_quota_fallback")
        elif profile.quota_category in {"orphan", "disability", "multichild", "single_parent"}:
            quota_factor = 0.10
            confidence = "low"
            confidence_reasons.append("social_quota_fallback")
        elif profile.quota_category == "targeted":
            if not (grants_now and grants_now.targeted_grants):
                confidence = "low"
                confidence_reasons.append("targeted_data_missing")

        score_margin = profile.total_score - weighted_cutoff
        raw = (score_margin / volatility) + math.log(max(grant_supply_factor, 0.01)) - math.log(max(demand_factor, 0.01)) + quota_factor
        probability = 1 / (1 + math.exp(-raw))

        if not grant_eligible:
            probability = 0.0

        probability_pct = int(round(probability * 100))
        if grant_eligible:
            probability_pct = max(1, min(probability_pct, 99))
        else:
            probability_pct = 0

        error_margin = 7 if confidence == "high" else 12 if confidence == "medium" else 20

        source_ids = {t.source_id for t in same_year_thresholds}
        source_ids.update({c.source_id for c in cutoffs})
        sources = []
        for source_id in sorted(source_ids):
            src = self.db.scalar(select(SourceDocument).where(SourceDocument.id == source_id))
            if src:
                sources.append({
                    "id": src.id,
                    "url": src.url,
                    "publisher": src.publisher,
                    "fetched_at": src.fetched_at.isoformat() if src.fetched_at else None,
                    "confidence": "high" if src.priority <= 2 else "medium" if src.priority <= 5 else "low",
                })

        return ForecastResult(
            grant_probability=probability_pct,
            paid_status="eligible" if paid_eligible else "not_eligible",
            grant_status="eligible_for_competition" if grant_eligible else "not_eligible",
            confidence=confidence,
            error_margin_pp=error_margin,
            explanation={
                "threshold_check": {
                    "grant_values": sorted(v for v in grant_values if v is not None),
                    "paid_values": sorted(v for v in paid_values if v is not None),
                    "grant_threshold_used": strict_grant_threshold,
                    "paid_threshold_used": paid_threshold,
                },
                "historical_cutoff": weighted_cutoff,
                "score_margin": score_margin,
                "grants_current_year": grants_now.total_grants if grants_now else None,
                "grants_previous_year": grants_prev.total_grants if grants_prev else None,
                "demand_factor": demand_factor,
                "quota_factor": quota_factor,
                "conflicts": ["Есть расхождение в источниках"] if has_conflict else [],
                "confidence_reasons": confidence_reasons,
            },
            sources=sources,
        )
