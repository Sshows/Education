from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.models import Order, PaymentWebhookEvent
from app.schemas.payments import (
    ConsumeCreditRequest,
    CreateOrderRequest,
    EntitlementOut,
    OrderOut,
    ProductOut,
    TelegramStarsConfirmRequest,
    TelegramStarsOrderRequest,
    WebhookOut,
)
from app.services.payments.errors import PaymentError
from app.services.payments.service import PaymentService

router = APIRouter(prefix="/api/payments", tags=["payments"])
admin_router = APIRouter(prefix="/api/admin/payments", tags=["admin-payments"])


def _handle_payment_error(exc: PaymentError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=str(exc))


def _product_out(product) -> ProductOut:
    return ProductOut(
        code=product.code,
        title_ru=product.title_ru,
        description_ru=product.description_ru,
        product_type=product.product_type,
        stars_price=product.stars_price,
        kzt_price=product.kzt_price,
        currency=product.currency,
        features=list(product.features_json or []),
        is_active=product.is_active,
    )


def _order_out(order, checkout=None, product=None, payment_instructions: str | None = None) -> OrderOut:
    product_code = product.code if product else "unknown"
    return OrderOut(
        order_id=order.id,
        status=order.status,
        provider=order.provider,
        product_code=product_code,
        amount=float(order.amount),
        currency=order.currency,
        checkout_url=order.checkout_url or (checkout.checkout_url if checkout else None),
        telegram_invoice_payload=checkout.telegram_invoice_payload if checkout else None,
        expires_at=order.expires_at,
        payment_instructions=payment_instructions,
    )


def _entitlement_out(entitlement) -> EntitlementOut:
    return EntitlementOut(
        product_code=entitlement.product_code,
        access_type=entitlement.access_type,
        credits_total=entitlement.credits_total,
        credits_used=entitlement.credits_used,
        starts_at=entitlement.starts_at,
        expires_at=entitlement.expires_at,
        is_active=entitlement.is_active,
    )


def _require_admin(x_admin_token: str | None = Header(default=None)) -> None:
    if not settings.session_secret or x_admin_token != settings.session_secret:
        raise HTTPException(status_code=401, detail="Admin auth required")


@router.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    service = PaymentService(db)
    return [_product_out(product) for product in service.list_products()]


@router.get("/products/{code}", response_model=ProductOut)
def get_product(code: str, db: Session = Depends(get_db)):
    service = PaymentService(db)
    try:
        return _product_out(service.get_product(code))
    except PaymentError as exc:
        _handle_payment_error(exc)


@router.post("/orders", response_model=OrderOut)
async def create_order(req: CreateOrderRequest, db: Session = Depends(get_db)):
    service = PaymentService(db)
    try:
        order, checkout = await service.create_order(
            product_code=req.product_code,
            provider=req.provider,
            telegram_id=req.telegram_id,
            return_url=req.return_url,
            metadata=req.metadata,
            idempotency_key=req.idempotency_key,
        )
        product = service.product_for_order(order)
        instructions = "Оплата внутри Telegram — Stars" if order.provider == "telegram_stars" else "Внешний checkout, если провайдер доступен"
        return _order_out(order, checkout, product, instructions)
    except PaymentError as exc:
        _handle_payment_error(exc)


@router.post("/telegram-stars/order", response_model=OrderOut)
async def create_telegram_stars_order(req: TelegramStarsOrderRequest, db: Session = Depends(get_db)):
    service = PaymentService(db)
    try:
        order, checkout = await service.create_order(
            product_code=req.product_code,
            provider="telegram_stars",
            telegram_id=req.telegram_id,
            metadata=req.metadata,
            idempotency_key=req.idempotency_key,
        )
        product = service.product_for_order(order)
        return _order_out(order, checkout, product, "Оплата внутри Telegram — Stars")
    except PaymentError as exc:
        _handle_payment_error(exc)


@router.post("/telegram-stars/confirm", response_model=OrderOut)
def confirm_telegram_stars_payment(req: TelegramStarsConfirmRequest, db: Session = Depends(get_db)):
    service = PaymentService(db)
    try:
        order, _ = service.confirm_telegram_stars_payment(
            order_id=req.order_id,
            telegram_id=req.telegram_id,
            total_amount=req.total_amount,
            currency=req.currency,
            telegram_payment_charge_id=req.telegram_payment_charge_id,
            provider_payment_id=req.provider_payment_id,
            raw_payload=req.raw_payload,
        )
        product = service.product_for_order(order)
        return _order_out(order, product=product, payment_instructions="Premium активирован")
    except PaymentError as exc:
        _handle_payment_error(exc)


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    service = PaymentService(db)
    try:
        order = service.get_order(order_id)
        product = service.product_for_order(order)
        return _order_out(order, product=product)
    except PaymentError as exc:
        _handle_payment_error(exc)


@router.get("/my-entitlements", response_model=list[EntitlementOut])
def my_entitlements(telegram_id: int | None = None, db: Session = Depends(get_db)):
    service = PaymentService(db)
    return [_entitlement_out(item) for item in service.list_entitlements(telegram_id=telegram_id)]


@router.post("/consume-credit", response_model=EntitlementOut)
def consume_credit(req: ConsumeCreditRequest, db: Session = Depends(get_db)):
    service = PaymentService(db)
    try:
        return _entitlement_out(service.consume_credit(req.telegram_id, req.feature, req.product_code))
    except PaymentError as exc:
        _handle_payment_error(exc)


async def _webhook(provider: str, request: Request, db: Session) -> WebhookOut:
    service = PaymentService(db)
    payload: dict[str, Any] = await request.json()
    headers = {key.lower(): value for key, value in request.headers.items()}
    try:
        event = await service.record_webhook(provider, payload, headers)
        return WebhookOut(ok=True, processed=event.processed, event_id=event.id, message="Webhook recorded")
    except PaymentError as exc:
        _handle_payment_error(exc)


@router.post("/webhooks/halyk", response_model=WebhookOut)
async def halyk_webhook(request: Request, db: Session = Depends(get_db)):
    return await _webhook("halyk_epay", request, db)


@router.post("/webhooks/freedom", response_model=WebhookOut)
async def freedom_webhook(request: Request, db: Session = Depends(get_db)):
    return await _webhook("freedom_pay", request, db)


@router.post("/webhooks/kaspi", response_model=WebhookOut)
async def kaspi_webhook(request: Request, db: Session = Depends(get_db)):
    return await _webhook("kaspi", request, db)


@router.post("/webhooks/crypto", response_model=WebhookOut)
async def crypto_webhook(request: Request, db: Session = Depends(get_db)):
    return await _webhook("crypto", request, db)


@router.post("/webhooks/aipay", response_model=WebhookOut)
async def aipay_webhook(request: Request, db: Session = Depends(get_db)):
    return await _webhook("aipay", request, db)


@admin_router.get("/orders", dependencies=[Depends(_require_admin)])
def admin_orders(db: Session = Depends(get_db)):
    orders = db.scalars(select(Order).order_by(Order.created_at.desc())).all()
    return [
        {
            "id": order.id,
            "provider": order.provider,
            "status": order.status,
            "amount": float(order.amount),
            "currency": order.currency,
            "telegram_id": order.telegram_id,
            "created_at": order.created_at,
        }
        for order in orders
    ]


@admin_router.get("/webhooks", dependencies=[Depends(_require_admin)])
def admin_webhooks(db: Session = Depends(get_db)):
    events = db.scalars(select(PaymentWebhookEvent).order_by(PaymentWebhookEvent.received_at.desc())).all()
    return [
        {
            "id": event.id,
            "provider": event.provider,
            "event_type": event.event_type,
            "provider_event_id": event.provider_event_id,
            "signature_valid": event.signature_valid,
            "processed": event.processed,
            "received_at": event.received_at,
            "error_message": event.error_message,
        }
        for event in events
    ]


@admin_router.post("/orders/{order_id}/refund", dependencies=[Depends(_require_admin)])
def admin_refund(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "paid":
        raise HTTPException(status_code=400, detail="Only paid orders can be refunded")
    order.status = "refunded"
    db.commit()
    return {"status": "refunded", "order_id": order_id}


@admin_router.post("/orders/{order_id}/grant-manual-access", dependencies=[Depends(_require_admin)])
def admin_manual_access(order_id: int, db: Session = Depends(get_db)):
    service = PaymentService(db)
    order = service.get_order(order_id)
    order.status = "paid"
    order.provider = "manual"
    db.commit()
    entitlement = service.grant_entitlement(order)
    return {"status": "granted", "order_id": order_id, "entitlement_id": entitlement.id}
