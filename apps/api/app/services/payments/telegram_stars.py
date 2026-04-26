from __future__ import annotations

from app.services.payments.base import CheckoutResult, PaymentStatusResult, PaymentWebhookResult, RefundResult, WebhookVerificationResult


class TelegramStarsProvider:
    provider_code = "telegram_stars"

    async def create_checkout(self, order) -> CheckoutResult:
        return CheckoutResult(
            provider=self.provider_code,
            order_id=order.id,
            status=order.status,
            telegram_invoice_payload=str(order.id),
            raw_response={"currency": "XTR", "amount": int(order.amount)},
        )

    async def verify_webhook(self, payload: dict, headers: dict) -> WebhookVerificationResult:
        return WebhookVerificationResult(
            signature_valid=True,
            provider_event_id=str(payload.get("telegram_payment_charge_id") or payload.get("provider_payment_id") or ""),
            event_type="successful_payment",
        )

    async def handle_webhook(self, payload: dict, headers: dict) -> PaymentWebhookResult:
        return PaymentWebhookResult(processed=True, status="paid", raw_response=payload)

    async def get_status(self, order) -> PaymentStatusResult:
        return PaymentStatusResult(status=order.status, provider_payment_id=order.provider_payment_id)

    async def refund(self, order, amount: float | None = None) -> RefundResult:
        return RefundResult(status="manual_required", amount=amount, raw_response={"reason": "Telegram Stars refunds require Bot API refund flow"})
