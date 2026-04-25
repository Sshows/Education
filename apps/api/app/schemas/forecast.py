from pydantic import BaseModel, Field


class ApplicantProfileIn(BaseModel):
    total_score: int = Field(ge=0, le=140)
    profile_subject_1: str
    profile_subject_2: str
    subject_combo: str
    language: str = "ru"
    quota_category: str = "ordinary"


class ForecastRequest(BaseModel):
    profile: ApplicantProfileIn
    university_id: int
    program_group_id: int


class ForecastResponse(BaseModel):
    grant_probability: int
    paid_status: str
    confidence: str
    error_margin_pp: int
    explanation: dict
    source_ids: list[int]
    status: str
