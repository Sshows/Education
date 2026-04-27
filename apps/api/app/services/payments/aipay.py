from __future__ import annotations

import httpx

from app.core.config import settings
from app.services.payments.base import CheckoutResult, PaymentStatusResult, PaymentWebhookResult, RefundResult, WebhookVerificationResult
from app.services.payments.errors import ProviderConfigurationError, ProviderDisabledError
from app.services.payments.signatures import verify_hmac_sha256


class AipayProvider:
    provider_code = "aipay"

    def _ensure_enabled(self) -> None:
        if not settings.payments_enable_aipay or not settings.aipay_enabled:
            raise ProviderDisabledError("AiPay is disabled. Use Telegram Stars or enable AiPay env flags.")
        if not settings.aipay_api_url or not settings.aipay_secret:
            raise ProviderConfigurationError("AiPay credentials are not configured.")

    async def create_checkout(self, order) -> CheckoutResult:
        self._ensure_enabled()
        endpoint = f"{settings.aipay_api_url.rstrip('/')}/invoices"
        payload = {
            "amount": int(order.amount),
            "currency": "KZT",
            "description": "Анализ шансов на грант BilimGrant",
            "external_id": str(order.id),
            "callback_url": settings.aipay_callback_url,
            "success_url": settings.aipay_success_url,
            "failure_url": settings.aipay_failure_url,
        }
        headers = {"Authorization": f"Bearer {settings.aipay_secret}"}
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.post(endpoint, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError as exc:
                raise ProviderConfigurationError("AiPay invoice request failed. Check AiPay API URL and credentials.") from exc

        checkout_url = data.get("payment_url") or data.get("checkout_url") or data.get("invoice_url") or data.get("url")
        if not checkout_url:
            raise ProviderConfigurationError("AiPay response does not include a checkout URL.")

        return CheckoutResult(
            provider=self.provider_code,
            order_id=order.id,
            status="pending",
            checkout_url=str(checkout_url),
            raw_response=data,
        )

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        signature = headers.get("x-aipay-signature") or headers.get("x-signature")
        event_id = payload.get("event_id") or payload.get("id") or payload.get("payment_id") or payload.get("external_id")
        status = str(payload.get("status") or payload.get("type") or "payment")
        return WebhookVerificationResult(
            signature_valid=verify_hmac_sha256(payload, signature, settings.aipay_secret),
            provider_event_id=str(event_id) if event_id else None,
            event_type=status,
            error_message=None if signature else "Missing AiPay signature",
        )

    async def handle_webhook(self, payload: dict, headers: dict) -> PaymentWebhookResult:
        status = str(payload.get("status") or "").lower()
        order_id = payload.get("external_id") or payload.get("order_id")
        if status in {"paid", "success", "completed", "approved"}:
            return PaymentWebhookResult(processed=True, order_id=int(order_id) if order_id else None, status="paid", raw_response=payload)
        if status in {"failed", "canceled", "cancelled", "expired"}:
            return PaymentWebhookResult(processed=True, order_id=int(order_id) if order_id else None, status="failed", raw_response=payload)
        return PaymentWebhookResult(processed=False, order_id=int(order_id) if order_id else None, status="pending", raw_response=payload)

    async def get_status(self, order) -> PaymentStatusResult:
        return PaymentStatusResult(status=order.status, provider_payment_id=order.provider_payment_id)

    async def refund(self, order, amount: float | None = None) -> RefundResult:
        self._ensure_enabled()
        return RefundResult(status="manual_required", amount=amount)
