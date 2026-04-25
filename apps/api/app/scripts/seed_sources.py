from sqlalchemy import select

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.models import (
    AdmissionThreshold,
    EducationProgram,
    GrantAllocation,
    HistoricalCutoff,
    ProgramGroup,
    SourceDocument,
    TuitionFee,
    University,
)

SEED_URLS = [
    ("NCT ENT", "https://testcenter.kz/?page_id=14510&lang=ru", "nct", "NCT", 1),
    ("NCT Rules", "https://testcenter.kz/?page_id=15617&lang=ru", "nct", "NCT", 1),
    ("NCT Grants", "https://grant.testcenter.kz/", "nct", "NCT", 1),
    ("eGov ENT", "https://egov.kz/cms/ru/articles/about_ent", "gov", "eGov", 3),
    ("MSHE news", "https://www.gov.kz/memleket/entities/sci/press/news/details/1047249?lang=ru", "gov", "MSHE", 2),
    ("ENIC registry", "https://enic-kazakhstan.edu.kz/ru/reestr-op/reestr-op-1", "registry", "ENIC", 4),
    ("EPVO", "https://epvo.kz/", "registry", "EPVO", 4),
    ("IITU minimum", "https://iitu.edu.kz/ru/articles/ac/bachelors-minimum-points/", "university", "IITU", 5),
    ("IITU prices", "https://iitu.edu.kz/ru/articles/ac/bachelors-prices/", "university", "IITU", 5),
    ("UniVision B057", "https://univision.kz/edu-program/group/B057-informatsionnye-tehnologii.html", "aggregator", "UniVision", 6),
]

PROGRAMS = [
    ("B057", "Информационные технологии", "Mathematics", "Informatics"),
    ("B058", "Информационная безопасность", "Mathematics", "Informatics"),
    ("B059", "Коммуникации и коммуникационные технологии", "Mathematics", "Physics"),
    ("B157", "Информационные системы и технологии", "Mathematics", "Informatics"),
]


def get_or_create_source(db, title, url, source_type, publisher, priority):
    src = db.scalar(select(SourceDocument).where(SourceDocument.url == url))
    if not src:
        src = SourceDocument(title=title, url=url, source_type=source_type, publisher=publisher, priority=priority, status="seeded")
        db.add(src)
        db.flush()
    return src


def run():
    Base.metadata.create_all(engine)
    db = SessionLocal()

    sources = {}
    for row in SEED_URLS:
        src = get_or_create_source(db, *row)
        sources[src.url] = src

    iitu = db.scalar(select(University).where(University.short_name == "IITU"))
    if not iitu:
        iitu = University(
            name_ru="Международный университет информационных технологий",
            short_name="IITU",
            city="Алматы",
            region="Алматы",
            ownership_type="private",
            official_website="https://iitu.edu.kz/",
            admissions_url="https://iitu.edu.kz/",
            source_priority=5,
        )
        db.add(iitu)
        db.flush()

    group_map = {}
    for code, name, s1, s2 in PROGRAMS:
        pg = db.scalar(select(ProgramGroup).where(ProgramGroup.code == code))
        if not pg:
            pg = ProgramGroup(code=code, name_ru=name, profile_subject_1=s1, profile_subject_2=s2, requires_creative_exam=False)
            db.add(pg)
            db.flush()
        group_map[code] = pg

    # education programs in IITU
    for code in ["B057", "B058", "B059", "B157"]:
        pg = group_map[code]
        exists = db.scalar(select(EducationProgram).where(EducationProgram.university_id == iitu.id, EducationProgram.program_group_id == pg.id, EducationProgram.code == code))
        if not exists:
            db.add(EducationProgram(university_id=iitu.id, program_group_id=pg.id, code=code, name_ru=pg.name_ru, degree="bachelor", duration_years=4, language="ru"))

    src_iitu = sources["https://iitu.edu.kz/ru/articles/ac/bachelors-minimum-points/"]
    src_uni = sources["https://univision.kz/edu-program/group/B057-informatsionnye-tehnologii.html"]
    src_price = sources["https://iitu.edu.kz/ru/articles/ac/bachelors-prices/"]

    b057 = group_map["B057"]
    for grant in [75, 80]:
        th = db.scalar(
            select(AdmissionThreshold).where(
                AdmissionThreshold.university_id == iitu.id,
                AdmissionThreshold.program_group_id == b057.id,
                AdmissionThreshold.year == 2025,
                AdmissionThreshold.grant_min_score == grant,
            )
        )
        if not th:
            db.add(
                AdmissionThreshold(
                    university_id=iitu.id,
                    program_group_id=b057.id,
                    year=2025,
                    grant_min_score=grant,
                    paid_min_score=50,
                    source_id=src_iitu.id,
                    confidence="medium",
                    is_conflict=True,
                    conflict_group="iitu_b057_2025",
                )
            )

    hc = db.scalar(select(HistoricalCutoff).where(HistoricalCutoff.university_id == iitu.id, HistoricalCutoff.program_group_id == b057.id, HistoricalCutoff.year == 2025))
    if not hc:
        db.add(HistoricalCutoff(year=2025, university_id=iitu.id, program_group_id=b057.id, contest_type="general", quota_category="ordinary", language="ru", min_score=90, grants_count=120, source_id=src_uni.id, source_priority=6, confidence="low"))

    ga = db.scalar(select(GrantAllocation).where(GrantAllocation.program_group_id == b057.id, GrantAllocation.year == 2025))
    if not ga:
        db.add(GrantAllocation(year=2025, program_group_id=b057.id, education_area="B057", total_grants=400, quota_grants=40, targeted_grants=10, source_id=src_iitu.id, is_project=False))

    tf = db.scalar(select(TuitionFee).where(TuitionFee.university_id == iitu.id, TuitionFee.program_group_id == b057.id, TuitionFee.year == 2025))
    if not tf:
        db.add(TuitionFee(university_id=iitu.id, program_group_id=b057.id, year=2025, degree="bachelor", duration_years=4, first_year_price_kzt=1400000, total_price_kzt=5600000, source_id=src_price.id))

    db.commit()
    db.close()


if __name__ == "__main__":
    run()
