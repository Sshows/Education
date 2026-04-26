"""Tests: subject pair matching, alias resolution, program validation."""
import pytest

from app.core.ent_subjects import (
    SubjectId,
    get_combination_by_alias,
    get_combination_by_pair,
    get_recommended_codes_for_pair,
    normalize_subject_id,
    normalize_subject_pair,
    program_matches_subject_pair,
    subject_pair_key,
    validate_subjects_for_program,
)


# ---------- normalize_subject_id ----------

def test_normalize_valid_subject():
    assert normalize_subject_id("mathematics") == "mathematics"
    assert normalize_subject_id("MATHEMATICS") == "mathematics"
    assert normalize_subject_id("biology") == "biology"


def test_normalize_unknown_subject_returns_none():
    assert normalize_subject_id("astrology") is None
    assert normalize_subject_id("") is None


# ---------- pair key order-insensitivity ----------

def test_pair_key_is_order_insensitive():
    assert subject_pair_key("biology", "chemistry") == subject_pair_key("chemistry", "biology")
    assert subject_pair_key("mathematics", "physics") == subject_pair_key("physics", "mathematics")
    assert subject_pair_key("mathematics", "informatics") == subject_pair_key("informatics", "mathematics")


def test_normalize_pair_order():
    a, b = normalize_subject_pair("chemistry", "biology")
    c, d = normalize_subject_pair("biology", "chemistry")
    assert subject_pair_key(a, b) == subject_pair_key(c, d)


# ---------- get_combination_by_pair ----------

def test_combination_bio_chem_equals_chem_bio():
    c1 = get_combination_by_pair("biology", "chemistry")
    c2 = get_combination_by_pair("chemistry", "biology")
    assert c1 is not None
    assert c2 is not None
    assert c1.key == c2.key


def test_combination_math_physics():
    combo = get_combination_by_pair("mathematics", "physics")
    assert combo is not None
    assert "физмат" in combo.aliases


def test_combination_unknown_pair_returns_none():
    result = get_combination_by_pair("geography", "informatics")
    assert result is None


# ---------- alias resolution ----------

def test_alias_infomatics_resolves():
    combo = get_combination_by_alias("инфомат")
    assert combo is not None
    assert "mathematics" in (combo.subject1, combo.subject2)
    assert "informatics" in (combo.subject1, combo.subject2)


def test_alias_fizmat_resolves():
    combo = get_combination_by_alias("физмат")
    assert combo is not None
    assert "mathematics" in (combo.subject1, combo.subject2)
    assert "physics" in (combo.subject1, combo.subject2)


def test_alias_khimbio_resolves():
    combo = get_combination_by_alias("химбио")
    assert combo is not None
    assert "biology" in (combo.subject1, combo.subject2)
    assert "chemistry" in (combo.subject1, combo.subject2)


def test_alias_biochem_same_as_khimbio():
    c1 = get_combination_by_alias("химбио")
    c2 = get_combination_by_alias("биохим")
    assert c1 is not None and c2 is not None
    assert c1.key == c2.key


def test_alias_creative_resolves():
    combo = get_combination_by_alias("творческий")
    assert combo is not None
    assert combo.subject1 == "creative_exam"


# ---------- program matching ----------

def test_b057_matches_math_informatics():
    assert program_matches_subject_pair("B057", "mathematics", "informatics") is True
    assert program_matches_subject_pair("B057", "informatics", "mathematics") is True


def test_b058_matches_math_informatics():
    assert program_matches_subject_pair("B058", "mathematics", "informatics") is True


def test_b057_rejects_bio_chem():
    assert program_matches_subject_pair("B057", "biology", "chemistry") is False


def test_b086_matches_bio_chem():
    assert program_matches_subject_pair("B086", "biology", "chemistry") is True
    assert program_matches_subject_pair("B086", "chemistry", "biology") is True


def test_b049_matches_law():
    assert program_matches_subject_pair("B049", "world_history", "fundamentals_of_law") is True
    assert program_matches_subject_pair("B049", "fundamentals_of_law", "world_history") is True


# ---------- validate_subjects_for_program ----------

def test_validate_b057_with_correct_subjects_returns_none():
    result = validate_subjects_for_program("B057", "mathematics", "informatics")
    assert result is None


def test_validate_b057_with_wrong_subjects_returns_message():
    result = validate_subjects_for_program("B057", "biology", "chemistry")
    assert result is not None
    assert "B057" in result
    assert "Математика" in result


def test_validate_unknown_program_returns_message():
    result = validate_subjects_for_program("ZZZ999", "mathematics", "physics")
    assert result is not None


# ---------- recommended codes ----------

def test_recommended_codes_for_infomatics():
    codes = get_recommended_codes_for_pair("mathematics", "informatics")
    assert "B057" in codes
    assert "B058" in codes
    assert "B059" in codes


def test_recommended_codes_for_law():
    codes = get_recommended_codes_for_pair("world_history", "fundamentals_of_law")
    assert "B049" in codes


# ---------- schema validation ----------

def test_applicant_profile_normalizes_subjects():
    from app.schemas.forecast import ApplicantProfileIn

    profile = ApplicantProfileIn(
        total_score=90,
        profile_subject_1="mathematics",
        profile_subject_2="informatics",
        subject_combo="",
    )
    assert profile.profile_subject_1 == "mathematics"
    assert profile.pair_key() == subject_pair_key("mathematics", "informatics")


def test_applicant_profile_rejects_invalid_subject():
    from pydantic import ValidationError

    from app.schemas.forecast import ApplicantProfileIn

    with pytest.raises(ValidationError):
        ApplicantProfileIn(
            total_score=90,
            profile_subject_1="astrology",
            profile_subject_2="informatics",
            subject_combo="",
        )
