# Payments architecture

ENT Grant is a Telegram Mini App first. Digital access inside Telegram should use Telegram Stars as the primary payment method.

## Products

| Code | Title | Type | Stars | KZT | Features |
| --- | --- | --- | ---: | ---: | --- |
| `free` | Бесплатно | one_time | 0 | 0 | basic calculator, catalog |
| `pro_once` | Полный прогноз | one_time | 50 | 490 | full forecast, recommendations, source breakdown |
| `ai_pack` | AI-пакет | consumable | 100 | 990 | 20 AI questions |
| `premium_month` | Premium на месяц | subscription | 250 | 1990 | unlimited forecasts, 100 AI questions, saved profile, alerts |

## Order model

1. Backend creates an `orders` record with an `idempotency_key`.
2. Provider checkout/invoice is created from that order.
3. Payment is not delivered after checkout creation.
4. A provider confirmation or webhook marks the order `paid`.
5. Backend writes `payments` and grants an `entitlements` row.
6. Duplicate confirms/webhooks must not duplicate entitlements.

Allowed status flow:

```text
created -> pending -> paid
created/pending -> failed/canceled/expired
paid -> refunded
```

`paid` cannot move back to `pending`.

## Telegram Stars

Stars is the primary method for digital goods inside Telegram. The bot creates an internal order through:

```text
POST /api/payments/telegram-stars/order
```

Then the bot sends a Telegram invoice. The entitlement is granted only after:

```text
POST /api/payments/telegram-stars/confirm
```

The confirmation must include the Telegram `telegram_payment_charge_id`, `total_amount`, `currency=XTR`, and internal order id from the invoice payload.

## External providers

Halyk ePay, Freedom Pay, Kaspi and Crypto are adapters behind feature flags. They are disabled until Railway env variables are configured.

External providers may create hosted checkout pages, but they must not activate access until status/webhook verification confirms payment.

Never:

- Store card data.
- Store crypto private keys.
- Accept screenshots as proof of payment.
- Grant access from an unverified callback.

## Webhooks

Webhook endpoints store raw payloads in `payment_webhook_events` for audit. Signature verification is required where provider support exists.

```text
POST /api/payments/webhooks/halyk
POST /api/payments/webhooks/freedom
POST /api/payments/webhooks/kaspi
POST /api/payments/webhooks/crypto
```

## Testing flow

1. `GET /api/payments/products`
2. `POST /api/payments/telegram-stars/order`
3. Bot sends invoice with `currency=XTR`
4. Bot receives `pre_checkout_query`
5. Bot receives `successful_payment`
6. Bot confirms backend order
7. `GET /api/payments/my-entitlements`

If payment passed but access is missing, use `/restore` in the bot or the `/support` page.
