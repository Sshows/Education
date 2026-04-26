"""
ENT Subject system — single source of truth for subject IDs, combinations,
aliases, and program-group mapping.

Mirrors packages/shared/src/ent-subjects.ts so both frontend and backend
share the same definitions without duplication.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Subject IDs
# ---------------------------------------------------------------------------

class SubjectId(str, Enum):
    # mandatory
    HISTORY_KAZAKHSTAN = "history_kazakhstan"
    MATH_LITERACY = "math_literacy"
    READING_LITERACY = "reading_literacy"
    # profile
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    INFORMATICS = "informatics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    GEOGRAPHY = "geography"
    WORLD_HISTORY = "world_history"
    FOREIGN_LANGUAGE = "foreign_language"
    FUNDAMENTALS_OF_LAW = "fundamentals_of_law"
    KAZAKH_LANGUAGE = "kazakh_language"
    RUSSIAN_LANGUAGE = "russian_language"
    KAZAKH_LITERATURE = "kazakh_literature"
    RUSSIAN_LITERATURE = "russian_literature"
    CREATIVE_EXAM = "creative_exam"


PROFILE_SUBJECT_IDS: Set[str] = {
    SubjectId.MATHEMATICS,
    SubjectId.PHYSICS,
    SubjectId.INFORMATICS,
    SubjectId.CHEMISTRY,
    SubjectId.BIOLOGY,
    SubjectId.GEOGRAPHY,
    SubjectId.WORLD_HISTORY,
    SubjectId.FOREIGN_LANGUAGE,
    SubjectId.FUNDAMENTALS_OF_LAW,
    SubjectId.KAZAKH_LANGUAGE,
    SubjectId.RUSSIAN_LANGUAGE,
    SubjectId.KAZAKH_LITERATURE,
    SubjectId.RUSSIAN_LITERATURE,
    SubjectId.CREATIVE_EXAM,
}

ALL_SUBJECT_IDS: Set[str] = PROFILE_SUBJECT_IDS | {
    SubjectId.HISTORY_KAZAKHSTAN,
    SubjectId.MATH_LITERACY,
    SubjectId.READING_LITERACY,
}


# ---------------------------------------------------------------------------
# Subject Combination
# ---------------------------------------------------------------------------

@dataclass
class SubjectCombination:
    key: str                  # canonical sorted key
    subject1: str
    subject2: str
    label_ru: str
    label_kk: str
    label_en: str
    aliases: List[str]
    category_ru: str
    category_en: str
    examples: List[str]
    program_group_codes: List[str]
    data_quality: str = "demo"


def _pair_key(a: str, b: str) -> str:
    """Build a canonical, order-insensitive key."""
    return "+".join(sorted([a, b]))


SUBJECT_COMBINATIONS: List[SubjectCombination] = [
    SubjectCombination(
        key=_pair_key("mathematics", "physics"),
        subject1="mathematics", subject2="physics",
        label_ru="Математика + Физика", label_kk="Математика + Физика", label_en="Mathematics + Physics",
        aliases=["физмат", "матфиз", "физ-мат", "мат-физ"],
        category_ru="Инженерия / технические науки", category_en="Engineering / Technical",
        examples=["Инженерия", "Строительство", "Энергетика", "Транспорт", "Горное дело"],
        program_group_codes=["B071", "B062", "B063", "B064", "B065", "B074", "B157"],
    ),
    SubjectCombination(
        key=_pair_key("mathematics", "informatics"),
        subject1="mathematics", subject2="informatics",
        label_ru="Математика + Информатика", label_kk="Математика + Информатика", label_en="Mathematics + Informatics",
        aliases=["инфомат", "матинф", "инф-мат", "мат-инф"],
        category_ru="IT / цифровые технологии", category_en="IT / Digital Technologies",
        examples=["B057 Информационные технологии", "B058 Информационная безопасность",
                  "B059 Коммуникации", "B157 Информационные системы"],
        program_group_codes=["B057", "B058", "B059", "B157"],
    ),
    SubjectCombination(
        key=_pair_key("mathematics", "geography"),
        subject1="mathematics", subject2="geography",
        label_ru="Математика + География", label_kk="Математика + География", label_en="Mathematics + Geography",
        aliases=["матгео", "геомат"],
        category_ru="Экономика / менеджмент / логистика", category_en="Economics / Management / Logistics",
        examples=["Экономика", "Менеджмент", "Финансы", "Учёт и аудит", "Туризм"],
        program_group_codes=["B044", "B045", "B046", "B047"],
    ),
    SubjectCombination(
        key=_pair_key("biology", "chemistry"),
        subject1="biology", subject2="chemistry",
        label_ru="Биология + Химия", label_kk="Биология + Химия", label_en="Biology + Chemistry",
        aliases=["химбио", "биохим", "хим-био", "био-хим"],
        category_ru="Медицина / биология / агрономия", category_en="Medicine / Biology / Agriculture",
        examples=["Медицина", "Стоматология", "Фармация", "Биология", "Ветеринария"],
        program_group_codes=["B084", "B085", "B086", "B087", "B088"],
    ),
    SubjectCombination(
        key=_pair_key("biology", "geography"),
        subject1="biology", subject2="geography",
        label_ru="Биология + География", label_kk="Биология + География", label_en="Biology + Geography",
        aliases=["биогео", "геобио"],
        category_ru="Педагогика / экология / география", category_en="Pedagogy / Ecology / Geography",
        examples=["Педагогика", "Экология", "География", "Природопользование"],
        program_group_codes=["B001", "B002", "B003"],
    ),
    SubjectCombination(
        key=_pair_key("foreign_language", "world_history"),
        subject1="foreign_language", subject2="world_history",
        label_ru="Иностранный язык + Всемирная история",
        label_kk="Шет тілі + Дүниежүзі тарихы",
        label_en="Foreign Language + World History",
        aliases=["англвсемирка", "ин язык всемирная история", "иняз всемирка"],
        category_ru="Языки / международные отношения", category_en="Languages / International Relations",
        examples=["Иностранная филология", "Переводческое дело", "Международные отношения"],
        program_group_codes=["B036", "B018"],
    ),
    SubjectCombination(
        key=_pair_key("foreign_language", "geography"),
        subject1="geography", subject2="foreign_language",
        label_ru="География + Иностранный язык", label_kk="География + Шет тілі", label_en="Geography + Foreign Language",
        aliases=["геоангл", "геоиняз"],
        category_ru="Туризм / международные программы", category_en="Tourism / International",
        examples=["Туризм", "Регионоведение"],
        program_group_codes=[],
    ),
    SubjectCombination(
        key=_pair_key("fundamentals_of_law", "world_history"),
        subject1="world_history", subject2="fundamentals_of_law",
        label_ru="Всемирная история + Основы права",
        label_kk="Дүниежүзі тарихы + Құқық негіздері",
        label_en="World History + Fundamentals of Law",
        aliases=["истправо", "всемирка право"],
        category_ru="Право / юриспруденция", category_en="Law / Jurisprudence",
        examples=["Право", "Юриспруденция"],
        program_group_codes=["B049"],
    ),
    SubjectCombination(
        key=_pair_key("geography", "world_history"),
        subject1="world_history", subject2="geography",
        label_ru="Всемирная история + География", label_kk="Дүниежүзі тарихы + География", label_en="World History + Geography",
        aliases=["истгео", "всемирка география"],
        category_ru="Гуманитарные / социальные науки", category_en="Humanities / Social Sciences",
        examples=["История", "Археология", "Регионоведение"],
        program_group_codes=[],
    ),
    SubjectCombination(
        key=_pair_key("kazakh_language", "kazakh_literature"),
        subject1="kazakh_language", subject2="kazakh_literature",
        label_ru="Казахский язык + Казахская литература",
        label_kk="Қазақ тілі + Қазақ әдебиеті",
        label_en="Kazakh Language + Kazakh Literature",
        aliases=["казлит", "казахский язык литература"],
        category_ru="Филология / языки", category_en="Philology / Languages",
        examples=["Филология", "Педагогика языка"],
        program_group_codes=["B037"],
    ),
    SubjectCombination(
        key=_pair_key("russian_language", "russian_literature"),
        subject1="russian_language", subject2="russian_literature",
        label_ru="Русский язык + Русская литература",
        label_kk="Орыс тілі + Орыс әдебиеті",
        label_en="Russian Language + Russian Literature",
        aliases=["руслит", "русский язык литература"],
        category_ru="Филология / языки", category_en="Philology / Languages",
        examples=["Филология", "Педагогика языка"],
        program_group_codes=["B037"],
    ),
    SubjectCombination(
        key=_pair_key("chemistry", "physics"),
        subject1="chemistry", subject2="physics",
        label_ru="Химия + Физика", label_kk="Химия + Физика", label_en="Chemistry + Physics",
        aliases=["химфиз", "физхим"],
        category_ru="Химическая инженерия / материалы", category_en="Chemical Engineering / Materials",
        examples=["Химическая инженерия", "Материаловедение"],
        program_group_codes=[],
    ),
    SubjectCombination(
        key=_pair_key("creative_exam", "creative_exam"),
        subject1="creative_exam", subject2="creative_exam",
        label_ru="Творческий экзамен", label_kk="Шығармашылық емтихан", label_en="Creative Exam",
        aliases=["творческий", "творч", "creative"],
        category_ru="Искусство / спорт / дизайн", category_en="Arts / Sport / Design",
        examples=["Дизайн", "Искусство", "Спорт"],
        program_group_codes=[],
    ),
]

# Build lookup maps at module load time
_KEY_MAP: Dict[str, SubjectCombination] = {c.key: c for c in SUBJECT_COMBINATIONS}
_ALIAS_MAP: Dict[str, str] = {}  # alias -> key
for _combo in SUBJECT_COMBINATIONS:
    for _alias in _combo.aliases:
        _ALIAS_MAP[_alias.lower().strip()] = _combo.key

# Program code -> combination key
_PROGRAM_MAP: Dict[str, str] = {}
for _combo in SUBJECT_COMBINATIONS:
    for _code in _combo.program_group_codes:
        _PROGRAM_MAP[_code] = _combo.key


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def normalize_subject_id(raw: str) -> Optional[str]:
    """Return a validated SubjectId string or None."""
    cleaned = raw.strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return SubjectId(cleaned).value
    except ValueError:
        return None


def normalize_subject_pair(a: str, b: str) -> Tuple[str, str]:
    """Return a sorted (a, b) tuple using canonical IDs."""
    id_a = normalize_subject_id(a) or a.lower().strip()
    id_b = normalize_subject_id(b) or b.lower().strip()
    return tuple(sorted([id_a, id_b]))  # type: ignore[return-value]


def subject_pair_key(a: str, b: str) -> str:
    """Canonical, order-insensitive pair key."""
    return _pair_key(a, b)


def get_combination_by_pair(subject1: str, subject2: str) -> Optional[SubjectCombination]:
    key = _pair_key(subject1, subject2)
    return _KEY_MAP.get(key)


def get_combination_by_alias(alias: str) -> Optional[SubjectCombination]:
    key = _ALIAS_MAP.get(alias.lower().strip())
    if key:
        return _KEY_MAP.get(key)
    return None


def normalize_alias_to_subjects(alias: str) -> Optional[Tuple[str, str]]:
    """Resolve an alias like 'инфомат' to ('informatics', 'mathematics')."""
    combo = get_combination_by_alias(alias)
    if combo:
        return (combo.subject1, combo.subject2)
    return None


def program_matches_subject_pair(program_code: str, subject1: str, subject2: str) -> bool:
    combo = get_combination_by_pair(subject1, subject2)
    if combo is None:
        return False
    return program_code in combo.program_group_codes


def validate_subjects_for_program(
    program_code: str, subject1: str, subject2: str
) -> Optional[str]:
    """
    Returns None if OK, or a Russian error message if subjects don't match
    the program requirements.
    """
    if program_matches_subject_pair(program_code, subject1, subject2):
        return None

    required_key = _PROGRAM_MAP.get(program_code)
    if not required_key:
        return f"Программа {program_code} не найдена в базе сочетаний. Проверьте код."

    required_combo = _KEY_MAP.get(required_key)
    label = required_combo.label_ru if required_combo else required_key
    user_key = _pair_key(subject1, subject2)
    return (
        f"Программа {program_code} требует: {label}. "
        f"Вы выбрали: {user_key}. "
        f"Исправьте профильные предметы или выберите другую программу."
    )


def get_recommended_codes_for_pair(subject1: str, subject2: str) -> List[str]:
    combo = get_combination_by_pair(subject1, subject2)
    return combo.program_group_codes if combo else []
