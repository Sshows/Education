from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.models import (AdmissionThreshold, GrantAllocation, HistoricalCutoff,
                               ProgramGroup, SourceDocument, University)

SEED_URLS = [
    ("NCT ENT", "https://testcenter.kz/?page_id=14510&lang=ru", "nct", "NCT", 1),
    ("NCT Grants", "https://grant.testcenter.kz/", "nct", "NCT", 1),
    ("eGov ENT", "https://egov.kz/cms/ru/articles/about_ent", "gov", "eGov", 2),
    ("ENIC registry", "https://enic-kazakhstan.edu.kz/ru/reestr-op/reestr-op-1", "registry", "ENIC", 4),
    ("IITU minimum", "https://iitu.edu.kz/ru/articles/ac/bachelors-minimum-points/", "university", "IITU", 5),
    ("UniVision B057", "https://univision.kz/edu-program/group/B057-informatsionnye-tehnologii.html", "aggregator", "UniVision", 6),
]


def run():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    for title, url, source_type, publisher, priority in SEED_URLS:
        if not db.query(SourceDocument).filter(SourceDocument.url == url).first():
            db.add(SourceDocument(title=title, url=url, source_type=source_type, publisher=publisher, priority=priority, status="seeded"))

    iitu = db.query(University).filter(University.short_name == "IITU").first()
    if not iitu:
        iitu = University(name_ru="Международный университет информационных технологий", short_name="IITU", city="Алматы", region="Алматы", ownership_type="private", official_website="https://iitu.edu.kz/", source_priority=5)
        db.add(iitu)
        db.flush()

    b057 = db.query(ProgramGroup).filter(ProgramGroup.code == "B057").first()
    if not b057:
        b057 = ProgramGroup(code="B057", name_ru="Информационные технологии", profile_subject_1="Mathematics", profile_subject_2="Informatics", requires_creative_exam=False)
        db.add(b057)
        db.flush()

    src_iitu = db.query(SourceDocument).filter(SourceDocument.url.like("%minimum-points%")) .first()
    src_uni = db.query(SourceDocument).filter(SourceDocument.url.like("%univision%")) .first()

    db.add_all([
        AdmissionThreshold(university_id=iitu.id, program_group_id=b057.id, year=2025, grant_min_score=75, paid_min_score=50, source_id=src_iitu.id, confidence="medium"),
        AdmissionThreshold(university_id=iitu.id, program_group_id=b057.id, year=2025, grant_min_score=80, paid_min_score=50, source_id=src_iitu.id, confidence="medium"),
        HistoricalCutoff(year=2025, university_id=iitu.id, program_group_id=b057.id, contest_type="general", quota_category="ordinary", language="ru", min_score=90, grants_count=120, source_id=src_uni.id, source_priority=6, confidence="low"),
        GrantAllocation(year=2025, program_group_id=b057.id, education_area="B057", total_grants=400, source_id=src_iitu.id, is_project=False),
    ])
    db.commit()
    db.close()


if __name__ == "__main__":
    run()
