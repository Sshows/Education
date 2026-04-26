from __future__ import annotations

from app.core.config import settings
from app.services.payments.base import CheckoutResult, PaymentStatusResult, PaymentWebhookResult, RefundResult, WebhookVerificationResult
from app.services.payments.errors import ProviderConfigurationError, ProviderDisabledError
from app.services.payments.signatures import verify_hmac_sha256


class CryptoProvider:
    provider_code = "crypto"

    def _ensure_enabled(self) -> None:
        if not settings.payments_enable_crypto or not settings.crypto_enabled:
            raise ProviderDisabledError("Crypto payments are disabled by default and require a regulated external provider.")
        if not settings.crypto_provider or not settings.crypto_api_key:
            raise ProviderConfigurationError("Crypto provider credentials are not configured.")

    async def create_checkout(self, order) -> CheckoutResult:
        self._ensure_enabled()
        raise ProviderConfigurationError("Crypto adapter intentionally avoids self-custody. Configure an external regulated provider first.")

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        signature = headers.get("x-crypto-signature") or headers.get("X-Crypto-Signature")
        return WebhookVerificationResult(
            signature_valid=verify_hmac_sha256(payload, signature, settings.crypto_webhook_secret),
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
