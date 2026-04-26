from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Entitlement, Order, Payment, PaymentProduct, PaymentWebhookEvent, User
from app.services.payments.base import CheckoutResult
from app.services.payments.crypto import CryptoProvider
from app.services.payments.errors import PaymentNotFoundError, PaymentValidationError, ProviderDisabledError
from app.services.payments.freedom_pay import FreedomPayProvider
from app.services.payments.halyk_epay import HalykEpayProvider
from app.services.payments.kaspi import KaspiProvider
from app.services.payments.telegram_stars import TelegramStarsProvider

DEFAULT_PRODUCTS = [
    {
        "code": "free",
        "title_ru": "Бесплатно",
        "title_kk": "Тегін",
        "title_en": "Free",
        "description_ru": "Базовый калькулятор, каталог программ и вузов.",
        "product_type": "one_time",
        "stars_price": 0,
        "kzt_price": 0,
        "currency": "XTR",
        "features_json": ["basic_calculator", "catalog"],
    },
    {
        "code": "pro_once",
        "title_ru": "Полный прогноз",
        "title_kk": "Толық болжам",
        "title_en": "Pro Forecast",
        "description_ru": "Расширенный прогноз, рекомендации, источники и сравнение score vs cutoff.",
        "product_type": "one_time",
        "stars_price": 50,
        "kzt_price": 490,
        "currency": "XTR",
        "features_json": ["full_forecast", "recommendations", "source_breakdown"],
    },
    {
        "code": "ai_pack",
        "title_ru": "AI-пакет",
        "title_kk": "AI пакеті",
        "title_en": "AI Pack",
        "description_ru": "20 вопросов AI-консультанту с ответами по источникам.",
        "product_type": "consumable",
        "stars_price": 100,
        "kzt_price": 990,
        "currency": "XTR",
        "features_json": ["ai_questions_20"],
    },
    {
        "code": "premium_month",
        "title_ru": "Premium на месяц",
        "title_kk": "Бір ай Premium",
        "title_en": "Monthly Premium",
        "description_ru": "Безлимитные прогнозы, 100 AI-вопросов, сохранённый профиль и уведомления.",
        "product_type": "subscription",
        "stars_price": 250,
        "kzt_price": 1990,
        "currency": "XTR",
        "features_json": ["unlimited_forecasts", "ai_questions_100", "saved_profile", "alerts"],
    },
]

PAID_STATUSES = {"paid", "refunded"}
FINAL_STATUSES = {"paid", "failed", "canceled", "expired", "refunded"}


class PaymentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.providers = {
            "telegram_stars": TelegramStarsProvider(),
            "halyk_epay": HalykEpayProvider(),
            "freedom_pay": FreedomPayProvider(),
            "kaspi": KaspiProvider(),
            "crypto": CryptoProvider(),
        }

    def ensure_default_products(self) -> None:
        for data in DEFAULT_PRODUCTS:
            product = self.db.scalar(select(PaymentProduct).where(PaymentProduct.code == data["code"]))
            if not product:
                product = PaymentProduct(**data, is_active=True)
                self.db.add(product)
                continue
            for key, value in data.items():
                setattr(product, key, value)
            product.is_active = True
        self.db.commit()

    def list_products(self) -> list[PaymentProduct]:
        self.ensure_default_products()
        return list(self.db.scalars(select(PaymentProduct).where(PaymentProduct.is_active.is_(True))).all())

    def get_product(self, code: str) -> PaymentProduct:
        self.ensure_default_products()
        product = self.db.scalar(select(PaymentProduct).where(PaymentProduct.code == code, PaymentProduct.is_active.is_(True)))
        if not product:
            raise PaymentNotFoundError("Product not found", status_code=404)
        return product

    def _find_user(self, telegram_id: int | None) -> User | None:
        if telegram_id is None:
            return None
        return self.db.scalar(select(User).where(User.telegram_id == telegram_id))

    def _amount_for_provider(self, product: PaymentProduct, provider: str) -> tuple[int, str]:
        if provider == "telegram_stars":
            if not settings.payments_enable_telegram_stars:
                raise ProviderDisabledError("Telegram Stars payments are disabled.")
            if not product.stars_price:
                raise PaymentValidationError("This product cannot be paid with Telegram Stars.")
            return int(product.stars_price), "XTR"

        if provider in {"halyk_epay", "freedom_pay", "kaspi"}:
            if provider == "halyk_epay" and (not settings.payments_enable_halyk or not settings.halyk_epay_enabled):
                raise ProviderDisabledError("Halyk ePay is disabled. Use Telegram Stars or enable Halyk env flags.")
            if provider == "freedom_pay" and (not settings.payments_enable_freedom or not settings.freedom_pay_enabled):
                raise ProviderDisabledError("Freedom Pay is disabled. Use Telegram Stars or enable Freedom Pay env flags.")
            if provider == "kaspi" and (not settings.payments_enable_kaspi or not settings.kaspi_enabled):
                raise ProviderDisabledError("Kaspi Pay пока не подключён. Используйте Telegram Stars или карту.")
            if provider == "halyk_epay" and (not settings.halyk_epay_terminal_id or not settings.halyk_epay_client_id or not settings.halyk_epay_client_secret):
                raise ProviderDisabledError("Halyk ePay credentials are not configured.")
            if provider == "freedom_pay" and (not settings.freedom_pay_merchant_id or not settings.freedom_pay_secret_key):
                raise ProviderDisabledError("Freedom Pay credentials are not configured.")
            if provider == "kaspi" and (not settings.kaspi_provider or not settings.kaspi_api_url or not settings.kaspi_api_key):
                raise ProviderDisabledError("Kaspi provider credentials are not configured.")
            if not product.kzt_price:
                raise PaymentValidationError("This product cannot be paid in KZT.")
            return int(product.kzt_price), "KZT"

        if provider == "crypto":
            raise ProviderDisabledError("Crypto payments are disabled by default and require an external regulated provider.")

        raise PaymentValidationError(f"Unsupported payment provider: {provider}")

    def _idempotency_key(self, product_code: str, provider: str, telegram_id: int | None, supplied: str | None, metadata: dict[str, Any]) -> str:
        if supplied:
            return supplied
        fingerprint = json.dumps(
            {"product_code": product_code, "provider": provider, "telegram_id": telegram_id, "metadata": metadata, "nonce": uuid4().hex},
            sort_keys=True,
        )
        return hashlib.sha256(fingerprint.encode()).hexdigest()

    async def create_order(
        self,
        product_code: str,
        provider: str,
        telegram_id: int | None = None,
        return_url: str | None = None,
        metadata: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> tuple[Order, CheckoutResult]:
        if not settings.payments_enabled:
            raise ProviderDisabledError("Payments are disabled.")

        metadata = metadata or {}
        product = self.get_product(product_code)
        key = self._idempotency_key(product_code, provider, telegram_id, idempotency_key, metadata)
        existing = self.db.scalar(select(Order).where(Order.idempotency_key == key))
        if existing:
            checkout = CheckoutResult(
                provider=existing.provider,
                order_id=existing.id,
                status=existing.status,
                checkout_url=existing.checkout_url,
                telegram_invoice_payload=str(existing.id) if existing.provider == "telegram_stars" else None,
                expires_at=existing.expires_at,
                raw_response={"idempotent": True},
            )
            return existing, checkout

        amount, currency = self._amount_for_provider(product, provider)
        user = self._find_user(telegram_id)
        expires_at = datetime.utcnow() + timedelta(minutes=30)
        order = Order(
            user_id=user.id if user else None,
            telegram_id=telegram_id,
            product_id=product.id,
            provider=provider,
            status="created",
            amount=Decimal(amount),
            currency=currency,
            idempotency_key=key,
            metadata_json={**metadata, "return_url": return_url},
            expires_at=expires_at,
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        provider_impl = self.providers.get(provider)
        if not provider_impl:
            raise PaymentValidationError(f"Unsupported payment provider: {provider}")
        checkout = await provider_impl.create_checkout(order)
        if checkout.checkout_url:
            order.checkout_url = checkout.checkout_url
        if order.status == "created":
            order.status = "pending"
        self.db.commit()
        self.db.refresh(order)
        checkout.status = order.status
        checkout.expires_at = order.expires_at
        return order, checkout

    def get_order(self, order_id: int) -> Order:
        order = self.db.get(Order, order_id)
        if not order:
            raise PaymentNotFoundError("Order not found", status_code=404)
        return order

    def product_for_order(self, order: Order) -> PaymentProduct:
        product = self.db.get(PaymentProduct, order.product_id)
        if not product:
            raise PaymentNotFoundError("Product not found", status_code=404)
        return product

    def _validate_status_transition(self, current: str, target: str) -> None:
        if current == target:
            return
        if current == "paid" and target != "refunded":
            raise PaymentValidationError("Paid orders cannot move back to a non-refund status.")
        if current in FINAL_STATUSES and current != "paid":
            raise PaymentValidationError(f"Order is already final: {current}")

    def grant_entitlement(self, order: Order) -> Entitlement:
        existing = self.db.scalar(select(Entitlement).where(Entitlement.source_order_id == order.id))
        if existing:
            return existing

        product = self.product_for_order(order)
        now = datetime.utcnow()
        credits_total: int | None = None
        expires_at = None
        access_type = product.product_type
        if product.code == "ai_pack":
            credits_total = 20
        elif product.code == "premium_month":
            credits_total = 100
            expires_at = now + timedelta(days=30)
        elif product.code == "pro_once":
            credits_total = 1

        entitlement = Entitlement(
            user_id=order.user_id,
            telegram_id=order.telegram_id,
            product_code=product.code,
            access_type=access_type,
            credits_total=credits_total,
            credits_used=0,
            starts_at=now,
            expires_at=expires_at,
            source_order_id=order.id,
            is_active=True,
        )
        self.db.add(entitlement)
        self.db.commit()
        self.db.refresh(entitlement)
        return entitlement

    def confirm_telegram_stars_payment(
        self,
        order_id: int,
        total_amount: int,
        currency: str,
        telegram_payment_charge_id: str,
        telegram_id: int | None = None,
        provider_payment_id: str | None = None,
        raw_payload: dict[str, Any] | None = None,
    ) -> tuple[Order, Entitlement]:
        order = self.get_order(order_id)
        product = self.product_for_order(order)
        if order.provider != "telegram_stars":
            raise PaymentValidationError("Order provider is not Telegram Stars.")
        if currency != "XTR" or order.currency != "XTR":
            raise PaymentValidationError("Telegram Stars payments must use XTR currency.")
        if int(order.amount) != int(total_amount):
            raise PaymentValidationError("Payment amount does not match order amount.")
        if product.stars_price != int(total_amount):
            raise PaymentValidationError("Payment amount does not match product price.")
        if telegram_id is not None and order.telegram_id is not None and order.telegram_id != telegram_id:
            raise PaymentValidationError("Telegram user does not match order.")

        self._validate_status_transition(order.status, "paid")
        order.status = "paid"
        order.telegram_id = telegram_id or order.telegram_id
        order.provider_payment_id = provider_payment_id or telegram_payment_charge_id
        order.paid_at = datetime.utcnow()
        payment = Payment(
            order_id=order.id,
            provider="telegram_stars",
            status="paid",
            amount=order.amount,
            currency="XTR",
            provider_payment_id=provider_payment_id or telegram_payment_charge_id,
            provider_charge_id=telegram_payment_charge_id,
            raw_payload_json=raw_payload or {},
            signature_valid=True,
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(order)
        return order, self.grant_entitlement(order)

    def list_entitlements(self, telegram_id: int | None = None, user_id: int | None = None) -> list[Entitlement]:
        stmt = select(Entitlement).where(Entitlement.is_active.is_(True))
        if telegram_id is not None:
            stmt = stmt.where(Entitlement.telegram_id == telegram_id)
        if user_id is not None:
            stmt = stmt.where(Entitlement.user_id == user_id)
        now = datetime.utcnow()
        entitlements = []
        for entitlement in self.db.scalars(stmt).all():
            if entitlement.expires_at and entitlement.expires_at < now:
                entitlement.is_active = False
                continue
            entitlements.append(entitlement)
        self.db.commit()
        return entitlements

    def has_entitlement(self, telegram_id: int | None, product_codes: set[str]) -> bool:
        return any(item.product_code in product_codes for item in self.list_entitlements(telegram_id=telegram_id))

    def consume_credit(self, telegram_id: int | None, feature: str, product_code: str | None = None) -> Entitlement:
        product_codes = [product_code] if product_code else ["ai_pack", "premium_month", "pro_once"]
        for entitlement in self.list_entitlements(telegram_id=telegram_id):
            if entitlement.product_code not in product_codes:
                continue
            if entitlement.credits_total is None or entitlement.credits_used < entitlement.credits_total:
                entitlement.credits_used += 1
                self.db.commit()
                self.db.refresh(entitlement)
                return entitlement
        raise PaymentValidationError(f"No active credits for feature: {feature}")

    async def record_webhook(self, provider: str, payload: dict[str, Any], headers: dict[str, str]) -> PaymentWebhookEvent:
        provider_impl = self.providers.get(provider)
        if not provider_impl:
            raise PaymentValidationError(f"Unsupported payment provider: {provider}")
        verification = await provider_impl.verify_webhook(payload, headers)
        existing = None
        if verification.provider_event_id:
            existing = self.db.scalar(
                select(PaymentWebhookEvent).where(
                    PaymentWebhookEvent.provider == provider,
                    PaymentWebhookEvent.provider_event_id == verification.provider_event_id,
                )
            )
        if existing:
            return existing

        event = PaymentWebhookEvent(
            provider=provider,
            event_type=verification.event_type,
            provider_event_id=verification.provider_event_id,
            signature_valid=verification.signature_valid,
            processed=False,
            raw_payload_json=payload,
            received_at=datetime.utcnow(),
            error_message=verification.error_message,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event
