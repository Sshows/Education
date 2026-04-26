from __future__ import annotations

from app.core.config import settings
from app.services.payments.base import CheckoutResult, PaymentStatusResult, PaymentWebhookResult, RefundResult, WebhookVerificationResult
from app.services.payments.errors import ProviderConfigurationError, ProviderDisabledError
from app.services.payments.signatures import verify_hmac_sha256


class HalykEpayProvider:
    provider_code = "halyk_epay"

    def _ensure_enabled(self) -> None:
        if not settings.payments_enable_halyk or not settings.halyk_epay_enabled:
            raise ProviderDisabledError("Halyk ePay is disabled. Use Telegram Stars or enable Halyk env flags.")
        if not settings.halyk_epay_terminal_id or not settings.halyk_epay_client_id or not settings.halyk_epay_client_secret:
            raise ProviderConfigurationError("Halyk ePay credentials are not configured.")

    async def create_checkout(self, order) -> CheckoutResult:
        self._ensure_enabled()
        raise ProviderConfigurationError("Halyk hosted checkout adapter is configured as a safe placeholder until merchant API details are provided.")

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        signature = headers.get("x-halyk-signature") or headers.get("X-Halyk-Signature")
        return WebhookVerificationResult(
            signature_valid=verify_hmac_sha256(payload, signature, settings.halyk_epay_webhook_secret),
            provider_event_id=str(payload.get("id") or payload.get("payment_id") or ""),
            event_type=str(payload.get("type") or "payment"),
        )

    async def handle_webhook(self, payload: dict, headers: dict) -> PaymentWebhookResult:
        return PaymentWebhookResult(processed=False, status="pending", raw_response=payload)

    async def get_status(self, order) -> PaymentStatusResult:
        return PaymentStatusResult(status=order.status, provider_payment_id=order.provider_payment_id)

    async def refund(self, order, amount: float | None = None) -> RefundResult:
        self._ensure_enabled()
        return RefundResult(status="manual_required", amount=amount)
