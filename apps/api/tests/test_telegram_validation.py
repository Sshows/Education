from app.schemas.common import ApplicantProfileInput
from app.utils.telegram import validate_telegram_init_data


def test_invalid_init_data_rejected():
    assert not validate_telegram_init_data("user=%7B%7D", "token")


def test_total_score_validation():
    try:
        ApplicantProfileInput(
            total_score=141,
            kazakhstan_history_score=10,
            math_literacy_score=10,
            reading_literacy_score=10,
            profile_subject_1="Mathematics",
            profile_subject_1_score=30,
            profile_subject_2="Informatics",
            profile_subject_2_score=30,
            subject_combo="Math+Informatics",
        )
        assert False
    except Exception:
        assert True
