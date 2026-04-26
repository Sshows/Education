# Telegram Stars

Telegram Stars is the primary payment method for digital features in this Mini App.

Official Telegram flow:

1. Bot sends invoice with `currency="XTR"`.
2. For digital goods, `provider_token` is empty.
3. Bot answers `pre_checkout_query` within 10 seconds.
4. Bot waits for `successful_payment`.
5. Backend confirms the internal order and grants entitlement.

## Bot flow

Commands:

```text
/premium
/buy
/payments
/restore
/support
```

Deep links:

```text
https://t.me/entgrant_kz_bot?start=buy_pro_once
https://t.me/entgrant_kz_bot?start=buy_ai_pack
https://t.me/entgrant_kz_bot?start=buy_premium_month
https://t.me/entgrant_kz_bot?start=pricing
```

Invoice details:

```text
currency=XTR
provider_token=""
prices=[single LabeledPrice]
payload=<internal order id>
```

Access is never granted after only `pre_checkout_query`.

## Backend endpoints

```text
POST /api/payments/telegram-stars/order
POST /api/payments/telegram-stars/confirm
GET /api/payments/products
GET /api/payments/my-entitlements
GET /api/payments/orders/{id}
```

## Checklist

1. Bot has `API_URL`.
2. API has `TELEGRAM_BOT_TOKEN`.
3. Bot webhook allowed updates include `pre_checkout_query`.
4. User opens `/premium`.
5. Bot sends Stars invoice.
6. `successful_payment` reaches webhook.
7. API order becomes `paid`.
8. Entitlement appears in profile/billing.
