from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol


@dataclass
class CheckoutResult:
    provider: str
    order_id: int
    status: str
    checkout_url: str | None = None
    telegram_invoice_payload: str | None = None
    expires_at: datetime | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class WebhookVerificationResult:
    signature_valid: bool
    provider_event_id: str | None = None
    event_type: str = "unknown"
    error_message: str | None = None


@dataclass
class PaymentWebhookResult:
    processed: bool
    order_id: int | None = None
    status: str = "ignored"
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class PaymentStatusResult:
    status: str
    provider_payment_id: str | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


@dataclass
class RefundResult:
    status: str
    amount: float | None = None
    raw_response: dict[str, Any] = field(default_factory=dict)


class PaymentProvider(Protocol):
    provider_code: str

    async def create_checkout(self, order) -> CheckoutResult:
        ...

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        ...

    async def handle_webhook(self, payload: dict, headers: dict) -> PaymentWebhookResult:
        ...

    async def get_status(self, order) -> PaymentStatusResult:
        ...

    async def refund(self, order, amount: float | None = None) -> RefundResult:
        ...
