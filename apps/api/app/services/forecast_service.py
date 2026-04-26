from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.core.ent_subjects import validate_subjects_for_program
from app.models.models import AdmissionThreshold, EntStatistics, GrantAllocation, HistoricalCutoff, ProgramGroup
from app.schemas.forecast import ApplicantProfileIn


@dataclass
class ForecastResult:
    grant_probability: int
    paid_status: str
    confidence: str
    error_margin_pp: int
    explanation: dict
    source_ids: list[int]
    status: str


class ForecastService:
    def __init__(self, db: Session):
        self.db = db

    def calculate(self, profile: ApplicantProfileIn, university_id: int, program_group_id: int) -> ForecastResult:
        pg = self.db.scalar(select(ProgramGroup).where(ProgramGroup.id == program_group_id))
        if not pg:
            raise ValueError("Program group not found")

        # Order-insensitive subject pair validation
        mismatch_msg = validate_subjects_for_program(
            pg.code,
            profile.profile_subject_1,
            profile.profile_subject_2,
        )
        if mismatch_msg:
            raise ValueError(mismatch_msg)

        threshold = self.db.scalar(
            select(AdmissionThreshold)
            .where(
                AdmissionThreshold.university_id == university_id,
                AdmissionThreshold.program_group_id == program_group_id,
            )
            .order_by(desc(AdmissionThreshold.year))
        )

        if not threshold:
            return ForecastResult(1, "unknown", "low", 25, {"reason": "нет подтверждённых данных"}, [], "insufficient_data")

        paid_eligible = profile.total_score >= (threshold.paid_min_score or 0)
        grant_eligible = profile.total_score >= (threshold.grant_min_score or 10**9)

        cutoffs = self.db.scalars(
            select(HistoricalCutoff)
            .where(
                HistoricalCutoff.university_id == university_id,
                HistoricalCutoff.program_group_id == program_group_id,
                HistoricalCutoff.year >= 2020,
                HistoricalCutoff.year <= 2025,
            )
            .order_by(HistoricalCutoff.year)
        ).all()

        grants_now = self.db.scalar(
            select(GrantAllocation)
            .where(GrantAllocation.program_group_id == program_group_id)
            .order_by(desc(GrantAllocation.year))
        )
        grants_prev = self.db.scalar(
            select(GrantAllocation)
            .where(GrantAllocation.program_group_id == program_group_id, GrantAllocation.year == (grants_now.year - 1 if grants_now else 2024))
        )

        demand_now = self.db.scalar(select(EntStatistics).where(EntStatistics.subject_combo == profile.subject_combo).order_by(desc(EntStatistics.year)))
        demand_prev = self.db.scalar(
            select(EntStatistics).where(
                EntStatistics.subject_combo == profile.subject_combo,
                EntStatistics.year == (demand_now.year - 1 if demand_now else 2024),
            )
        )

        if cutoffs:
            historical_scores = [c.min_score for c in cutoffs]
            weighted_cutoff = float(np.mean(historical_scores))
            volatility = max(float(np.std(historical_scores)), 1.0)
        else:
            weighted_cutoff = float(threshold.grant_min_score or profile.total_score)
            volatility = 14.0

        if len(cutoffs) >= 3 and grants_now and demand_now:
            confidence = "high"
            error_margin = 7
        elif len(cutoffs) >= 1:
            confidence = "medium"
            error_margin = 12
        else:
            confidence = "low"
            error_margin = 20

        grant_supply_factor = 1.0
        if grants_now and grants_prev and grants_now.total_grants and grants_prev.total_grants:
            grant_supply_factor = grants_now.total_grants / max(grants_prev.total_grants, 1)

        demand_factor = 1.0
        if demand_now and demand_prev and demand_now.participants_count and demand_prev.participants_count:
            demand_factor = demand_now.participants_count / max(demand_prev.participants_count, 1)

        quota_factor = 0.0
        if profile.quota_category == "rural":
            quota_factor = 0.15
        elif profile.quota_category in {"orphan", "disability", "multichild", "single_parent"}:
            quota_factor = 0.10
            if confidence == "high":
                confidence = "medium"

        score_margin = profile.total_score - weighted_cutoff
        raw = (score_margin / volatility) + math.log(max(grant_supply_factor, 0.01)) - math.log(max(demand_factor, 0.01)) + quota_factor
        probability = 1 / (1 + math.exp(-raw))

        if not grant_eligible:
            probability = 0
        elif probability > 0 and confidence == "low":
            probability = max(probability, 0.01)

        probability_pct = min(max(int(round(probability * 100)), 0), 99)
        source_ids = [threshold.source_id] + [c.source_id for c in cutoffs]

        explanation = {
            "subject_pair_key": profile.pair_key(),
            "threshold_check": {
                "grant_min_score": threshold.grant_min_score,
                "paid_min_score": threshold.paid_min_score,
                "grant_eligible": grant_eligible,
                "paid_eligible": paid_eligible,
            },
            "historical_cutoff": weighted_cutoff,
            "user_score_margin": score_margin,
            "grants_current_year": grants_now.total_grants if grants_now else None,
            "grants_previous_year": grants_prev.total_grants if grants_prev else None,
            "demand_factor": demand_factor,
            "quota_factor": quota_factor,
            "confidence_reasons": [
                f"historical_years={len(cutoffs)}",
                f"has_grants={bool(grants_now)}",
                f"has_demand={bool(demand_now)}",
            ],
            "source_ids": source_ids,
        }

        return ForecastResult(
            grant_probability=probability_pct,
            paid_status="eligible" if paid_eligible else "not_eligible",
            confidence=confidence,
            error_margin_pp=error_margin,
            explanation=explanation,
            source_ids=source_ids,
            status="eligible_for_competition" if grant_eligible else "not_eligible",
        )
