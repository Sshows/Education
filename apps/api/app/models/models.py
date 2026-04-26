from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, TimestampMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str | None] = mapped_column(String(16), nullable=True)


class ApplicantProfile(Base, TimestampMixin):
    __tablename__ = "applicant_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    total_score: Mapped[int] = mapped_column(Integer)
    kazakhstan_history_score: Mapped[int] = mapped_column(Integer)
    math_literacy_score: Mapped[int] = mapped_column(Integer)
    reading_literacy_score: Mapped[int] = mapped_column(Integer)
    profile_subject_1: Mapped[str] = mapped_column(String(128))
    profile_subject_1_score: Mapped[int] = mapped_column(Integer)
    profile_subject_2: Mapped[str] = mapped_column(String(128))
    profile_subject_2_score: Mapped[int] = mapped_column(Integer)
    subject_combo: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(128))
    locality_type: Mapped[str] = mapped_column(String(16))
    quota_category: Mapped[str] = mapped_column(String(64))
    language: Mapped[str] = mapped_column(String(16))
    target_degree: Mapped[str] = mapped_column(String(16))


class University(Base, TimestampMixin):
    __tablename__ = "universities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name_ru: Mapped[str] = mapped_column(String(255))
    name_kk: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    short_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    city: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(128))
    ownership_type: Mapped[str] = mapped_column(String(32))
    official_website: Mapped[str | None] = mapped_column(String(512), nullable=True)
    admissions_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    source_priority: Mapped[int] = mapped_column(Integer, default=5)
    last_verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ProgramGroup(Base, TimestampMixin):
    __tablename__ = "program_groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    name_ru: Mapped[str] = mapped_column(String(255))
    name_kk: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    education_area_code: Mapped[str | None] = mapped_column(String(32), nullable=True)
    education_area_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    profile_subject_1: Mapped[str] = mapped_column(String(128))
    profile_subject_2: Mapped[str] = mapped_column(String(128))
    requires_creative_exam: Mapped[bool] = mapped_column(Boolean, default=False)


class EducationProgram(Base, TimestampMixin):
    __tablename__ = "education_programs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"))
    program_group_id: Mapped[int] = mapped_column(ForeignKey("program_groups.id"))
    code: Mapped[str] = mapped_column(String(64))
    name_ru: Mapped[str] = mapped_column(String(255))
    name_kk: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree: Mapped[str] = mapped_column(String(32))
    duration_years: Mapped[float] = mapped_column(Float)
    language: Mapped[str] = mapped_column(String(16))


class SourceDocument(Base, TimestampMixin):
    __tablename__ = "source_documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(1024), unique=True)
    source_type: Mapped[str] = mapped_column(String(64))
    publisher: Mapped[str] = mapped_column(String(255))
    priority: Mapped[int] = mapped_column(Integer)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class AdmissionThreshold(Base, TimestampMixin):
    __tablename__ = "admission_thresholds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"), index=True)
    program_group_id: Mapped[int] = mapped_column(ForeignKey("program_groups.id"), index=True)
    year: Mapped[int] = mapped_column(Integer)
    grant_min_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    paid_min_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shortened_grant_min_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shortened_paid_min_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"))
    confidence: Mapped[str] = mapped_column(String(16), default="medium")


class GrantAllocation(Base, TimestampMixin):
    __tablename__ = "grant_allocations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    program_group_id: Mapped[int] = mapped_column(ForeignKey("program_groups.id"))
    education_area: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_time_grants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shortened_grants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quota_grants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    targeted_grants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_grants: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"))
    is_project: Mapped[bool] = mapped_column(Boolean, default=False)


class HistoricalCutoff(Base, TimestampMixin):
    __tablename__ = "historical_cutoffs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"))
    program_group_id: Mapped[int] = mapped_column(ForeignKey("program_groups.id"))
    contest_type: Mapped[str] = mapped_column(String(64))
    quota_category: Mapped[str] = mapped_column(String(64), default="ordinary")
    language: Mapped[str] = mapped_column(String(16), default="ru")
    min_score: Mapped[int] = mapped_column(Integer)
    grants_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"))
    source_priority: Mapped[int] = mapped_column(Integer, default=6)
    confidence: Mapped[str] = mapped_column(String(16), default="low")


class EntStatistics(Base, TimestampMixin):
    __tablename__ = "ent_statistics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    period: Mapped[str] = mapped_column(String(32))
    subject_combo: Mapped[str] = mapped_column(String(128))
    region: Mapped[str] = mapped_column(String(128))
    participants_count: Mapped[int] = mapped_column(Integer)
    average_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    threshold_passed_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"))


class ForecastRun(Base):
    __tablename__ = "forecast_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    applicant_profile_id: Mapped[int] = mapped_column(ForeignKey("applicant_profiles.id"))
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"))
    program_group_id: Mapped[int] = mapped_column(ForeignKey("program_groups.id"))
    total_score: Mapped[int] = mapped_column(Integer)
    predicted_grant_probability: Mapped[float] = mapped_column(Float)
    predicted_paid_status: Mapped[str] = mapped_column(String(64))
    confidence: Mapped[str] = mapped_column(String(16))
    error_margin_pp: Mapped[int] = mapped_column(Integer)
    explanation_json: Mapped[dict] = mapped_column(JSON)
    source_ids_json: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TuitionFee(Base, TimestampMixin):
    __tablename__ = "tuition_fees"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(ForeignKey("universities.id"))
    program_group_id: Mapped[int] = mapped_column(ForeignKey("program_groups.id"))
    year: Mapped[int] = mapped_column(Integer)
    degree: Mapped[str] = mapped_column(String(32))
    duration_years: Mapped[float] = mapped_column(Float)
    first_year_price_kzt: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_price_kzt: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"))


class QuotaType(Base, TimestampMixin):
    __tablename__ = "quota_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True)
    name_ru: Mapped[str] = mapped_column(String(255))
    name_kk: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    required_documents: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source_documents.id"))


class AdminUser(Base):
    __tablename__ = "admin_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    role: Mapped[str] = mapped_column(String(64), default="editor")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PaymentProduct(Base, TimestampMixin):
    __tablename__ = "payment_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title_ru: Mapped[str] = mapped_column(String(255))
    title_kk: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    product_type: Mapped[str] = mapped_column(String(32))
    stars_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    kzt_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    currency: Mapped[str] = mapped_column(String(8), default="XTR")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    features_json: Mapped[list] = mapped_column(JSON, default=list)


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("payment_products.id"))
    provider: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), default="created", index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8))
    provider_order_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_payment_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    checkout_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), index=True)
    provider: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8))
    provider_payment_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_charge_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    signature_valid: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Entitlement(Base, TimestampMixin):
    __tablename__ = "entitlements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    product_code: Mapped[str] = mapped_column(String(64), index=True)
    access_type: Mapped[str] = mapped_column(String(32))
    credits_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    credits_used: Mapped[int] = mapped_column(Integer, default=0)
    starts_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    source_order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PaymentWebhookEvent(Base):
    __tablename__ = "payment_webhook_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(32), index=True)
    event_type: Mapped[str] = mapped_column(String(64))
    provider_event_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    signature_valid: Mapped[bool] = mapped_column(Boolean, default=False)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    raw_payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


Index("ix_payment_webhook_events_provider_event", PaymentWebhookEvent.provider, PaymentWebhookEvent.provider_event_id)
