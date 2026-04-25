from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.models.models import AdmissionThreshold, GrantAllocation, HistoricalCutoff, ProgramGroup, SourceDocument
from app.schemas.common import ApplicantProfileInput
from app.services.forecast_service import ForecastService


def setup_db(with_conflict: bool = True, with_history: bool = True):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = Session(engine)
    src = SourceDocument(title="s", url="https://a", source_type="official", publisher="NCT", priority=1, status="parsed")
    src2 = SourceDocument(title="s2", url="https://b", source_type="secondary", publisher="UniVision", priority=6, status="parsed")
    db.add_all([src, src2])
    db.flush()
    pg = ProgramGroup(code="B057", name_ru="IT", profile_subject_1="Mathematics", profile_subject_2="Informatics", requires_creative_exam=False)
    db.add(pg)
    db.flush()
    db.add(AdmissionThreshold(university_id=1, program_group_id=pg.id, year=2025, grant_min_score=75, paid_min_score=50, source_id=src.id, is_conflict=with_conflict))
    if with_conflict:
        db.add(AdmissionThreshold(university_id=1, program_group_id=pg.id, year=2025, grant_min_score=80, paid_min_score=50, source_id=src.id, is_conflict=True))
    if with_history:
        db.add(HistoricalCutoff(year=2025, university_id=1, program_group_id=pg.id, contest_type="general", quota_category="ordinary", language="ru", min_score=90, source_id=src2.id, source_priority=6, confidence="low"))
    db.add(GrantAllocation(year=2025, program_group_id=pg.id, total_grants=200, source_id=src.id, is_project=False))
    db.commit()
    return db, pg.id


def profile(score: int = 82):
    return ApplicantProfileInput(
        total_score=score,
        kazakhstan_history_score=10,
        math_literacy_score=10,
        reading_literacy_score=10,
        profile_subject_1="Mathematics",
        profile_subject_1_score=30,
        profile_subject_2="Informatics",
        profile_subject_2_score=30,
        subject_combo="Math+Informatics",
        region="Алматы",
        locality_type="city",
        quota_category="ordinary",
        language="ru",
        target="both",
    )


def test_82_iitu_b057_low_grant_paid_eligible():
    db, pg_id = setup_db(with_conflict=False, with_history=True)
    res = ForecastService(db).calculate(profile(82), 1, pg_id)
    assert res.paid_status == "eligible"
    assert res.grant_probability < 50


def test_below_threshold_zero_probability():
    db, pg_id = setup_db(with_conflict=False, with_history=True)
    res = ForecastService(db).calculate(profile(60), 1, pg_id)
    assert res.grant_probability == 0


def test_conflict_reduces_confidence():
    db, pg_id = setup_db(with_conflict=True, with_history=True)
    res = ForecastService(db).calculate(profile(82), 1, pg_id)
    assert res.confidence == "low"
    assert res.explanation["conflicts"]


def test_missing_history_low_confidence():
    db, pg_id = setup_db(with_conflict=False, with_history=False)
    res = ForecastService(db).calculate(profile(82), 1, pg_id)
    assert res.confidence == "low"


def test_invalid_subject_scores_validation_error():
    db, pg_id = setup_db(with_conflict=False, with_history=True)
    bad = profile(82)
    bad.profile_subject_1_score = 4
    try:
        ForecastService(db).calculate(bad, 1, pg_id)
        assert False
    except ValueError:
        assert True
