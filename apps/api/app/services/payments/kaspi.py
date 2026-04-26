from __future__ import annotations

from app.core.config import settings
from app.services.payments.base import CheckoutResult, PaymentStatusResult, PaymentWebhookResult, RefundResult, WebhookVerificationResult
from app.services.payments.errors import ProviderConfigurationError, ProviderDisabledError
from app.services.payments.signatures import verify_hmac_sha256


class KaspiProvider:
    provider_code = "kaspi"

    def _ensure_enabled(self) -> None:
        if not settings.payments_enable_kaspi or not settings.kaspi_enabled:
            raise ProviderDisabledError("Kaspi Pay пока не подключён. Используйте Telegram Stars или карту.")
        if not settings.kaspi_provider or not settings.kaspi_api_url or not settings.kaspi_api_key:
            raise ProviderConfigurationError("Kaspi provider credentials are not configured.")

    async def create_checkout(self, order) -> CheckoutResult:
        self._ensure_enabled()
        raise ProviderConfigurationError("Kaspi adapter supports only confirmed official/provider invoice or QR APIs; configure provider details first.")

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        signature = headers.get("x-kaspi-signature") or headers.get("X-Kaspi-Signature")
        return WebhookVerificationResult(
            signature_valid=verify_hmac_sha256(payload, signature, settings.kaspi_webhook_secret),
            provider_event_id=str(payload.get("invoice_id") or payload.get("payment_id") or ""),
            event_type=str(payload.get("status") or "payment"),
        )

    async def handle_webhook(self, payload: dict, headers: dict) -> PaymentWebhookResult:
        return PaymentWebhookResult(processed=False, status="pending", raw_response=payload)

    async def get_status(self, order) -> PaymentStatusResult:
        return PaymentStatusResult(status=order.status, provider_payment_id=order.provider_payment_id)

    async def refund(self, order, amount: float | None = None) -> RefundResult:
        self._ensure_enabled()
        return RefundResult(status="manual_required", amount=amount)
