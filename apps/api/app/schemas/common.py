from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ApplicantProfileInput(BaseModel):
    total_score: int = Field(ge=0, le=140)
    kazakhstan_history_score: int = Field(ge=0, le=20)
    math_literacy_score: int = Field(ge=0, le=20)
    reading_literacy_score: int = Field(ge=0, le=20)
    profile_subject_1: str
    profile_subject_1_score: int = Field(ge=0, le=50)
    profile_subject_2: str
    profile_subject_2_score: int = Field(ge=0, le=50)
    subject_combo: str
    region: str = "Алматы"
    locality_type: Literal["city", "rural"] = "city"
    quota_category: str = "ordinary"
    language: str = "ru"
    target: Literal["grant", "paid", "both"] = "both"


class ForecastRequest(BaseModel):
    profile: ApplicantProfileInput
    university_id: int
    program_group_id: int


class ForecastResponse(BaseModel):
    grant_probability: int
    paid_status: Literal["eligible", "not_eligible", "unknown"]
    grant_status: Literal["eligible_for_competition", "not_eligible", "unknown"]
    confidence: Literal["high", "medium", "low"]
    error_margin_pp: int
    explanation: dict
    sources: list[dict]


class UniversityResponse(BaseModel):
    id: int
    name_ru: str
    city: str
    ownership_type: str
    official_website: str | None


class ProgramGroupResponse(BaseModel):
    id: int
    code: str
    name_ru: str
    profile_subject_1: str
    profile_subject_2: str


class SourceDocumentResponse(BaseModel):
    id: int
    title: str
    url: str
    publisher: str
    priority: int
    status: str
    fetched_at: datetime | None


class AIChatRequest(BaseModel):
    question: str


class AIChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    updated_at: datetime | None = None
