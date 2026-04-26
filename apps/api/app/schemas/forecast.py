from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from app.core.ent_subjects import normalize_subject_id, normalize_subject_pair, subject_pair_key


class ApplicantProfileIn(BaseModel):
    total_score: int = Field(ge=0, le=140)
    profile_subject_1: str
    profile_subject_2: str
    # subject_combo can be an alias (e.g. "инфомат") or a canonical pair key
    subject_combo: str = ""
    language: str = "ru"
    quota_category: str = "ordinary"

    @field_validator("profile_subject_1", "profile_subject_2", mode="before")
    @classmethod
    def validate_subject(cls, v: str) -> str:
        normalized = normalize_subject_id(v)
        if normalized is None:
            raise ValueError(
                f"Неизвестный предмет ЕНТ: '{v}'. "
                "Используйте корректный идентификатор (например: mathematics, biology, informatics)."
            )
        return normalized

    def normalized_pair(self) -> tuple[str, str]:
        return normalize_subject_pair(self.profile_subject_1, self.profile_subject_2)

    def pair_key(self) -> str:
        return subject_pair_key(self.profile_subject_1, self.profile_subject_2)


class ForecastRequest(BaseModel):
    profile: ApplicantProfileIn
    university_id: int
    program_group_id: int


class SubjectMismatchDetail(BaseModel):
    message_ru: str
    selected_subjects: list[str]
    required_subjects: str


class ForecastResponse(BaseModel):
    grant_probability: int
    paid_status: str
    confidence: str
    error_margin_pp: int
    explanation: dict
    source_ids: list[int]
    status: str
    subject_pair_key: str = ""
