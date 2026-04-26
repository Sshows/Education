from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


PaymentProviderCode = Literal["telegram_stars", "halyk_epay", "freedom_pay", "kaspi", "crypto", "manual"]


class ProductOut(BaseModel):
    code: str
    title_ru: str
    description_ru: str | None = None
    product_type: str
    stars_price: int | None = None
    kzt_price: int | None = None
    currency: str
    features: list[str]
    is_active: bool


class CreateOrderRequest(BaseModel):
    product_code: str
    provider: PaymentProviderCode = "telegram_stars"
    telegram_id: int | None = None
    return_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None


class OrderOut(BaseModel):
    order_id: int
    status: str
    provider: str
    product_code: str
    amount: float
    currency: str
    checkout_url: str | None = None
    telegram_invoice_payload: str | None = None
    expires_at: datetime | None = None
    payment_instructions: str | None = None


class TelegramStarsOrderRequest(BaseModel):
    product_code: str
    telegram_id: int | None = None
    idempotency_key: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TelegramStarsConfirmRequest(BaseModel):
    order_id: int
    telegram_id: int | None = None
    total_amount: int
    currency: str = "XTR"
    telegram_payment_charge_id: str
    provider_payment_id: str | None = None
    raw_payload: dict[str, Any] = Field(default_factory=dict)


class EntitlementOut(BaseModel):
    product_code: str
    access_type: str
    credits_total: int | None
    credits_used: int
    starts_at: datetime
    expires_at: datetime | None = None
    is_active: bool


class ConsumeCreditRequest(BaseModel):
    feature: str = "ai_questions"
    telegram_id: int | None = None
    product_code: str | None = None


class WebhookOut(BaseModel):
    ok: bool
    processed: bool
    event_id: int | None = None
    message: str = ""
