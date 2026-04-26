from __future__ import annotations

from app.core.config import settings
from app.services.payments.base import CheckoutResult, PaymentStatusResult, PaymentWebhookResult, RefundResult, WebhookVerificationResult
from app.services.payments.errors import ProviderConfigurationError, ProviderDisabledError
from app.services.payments.signatures import verify_hmac_sha256


class FreedomPayProvider:
    provider_code = "freedom_pay"

    def _ensure_enabled(self) -> None:
        if not settings.payments_enable_freedom or not settings.freedom_pay_enabled:
            raise ProviderDisabledError("Freedom Pay is disabled. Use Telegram Stars or enable Freedom Pay env flags.")
        if not settings.freedom_pay_merchant_id or not settings.freedom_pay_secret_key:
            raise ProviderConfigurationError("Freedom Pay credentials are not configured.")

    async def create_checkout(self, order) -> CheckoutResult:
        self._ensure_enabled()
        raise ProviderConfigurationError("Freedom Pay hosted checkout adapter is a safe placeholder until merchant API details are confirmed.")

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        signature = headers.get("x-freedom-signature") or headers.get("X-Freedom-Signature")
        return WebhookVerificationResult(
            signature_valid=verify_hmac_sha256(payload, signature, settings.freedom_pay_secret_key),
            provider_event_id=str(payload.get("pg_payment_id") or payload.get("payment_id") or ""),
            event_type=str(payload.get("pg_result") or payload.get("type") or "payment"),
        )

    async def handle_webhook(self, payload: dict, headers: dict) -> PaymentWebhookResult:
        return PaymentWebhookResult(processed=False, status="pending", raw_response=payload)

    async def get_status(self, order) -> PaymentStatusResult:
        return PaymentStatusResult(status=order.status, provider_payment_id=order.provider_payment_id)

    async def refund(self, order, amount: float | None = None) -> RefundResult:
        self._ensure_enabled()
        return RefundResult(status="manual_required", amount=amount)
