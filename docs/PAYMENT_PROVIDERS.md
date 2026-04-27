# Payment provider adapters

External providers are optional. Telegram Stars remains primary inside Telegram for digital access.

## Halyk ePay

Use hosted payment page or widget first. Do not implement direct card APIs unless PCI DSS requirements are confirmed.

Env:

```text
HALYK_EPAY_ENABLED=false
HALYK_EPAY_TEST_MODE=true
HALYK_EPAY_TERMINAL_ID=
HALYK_EPAY_CLIENT_ID=
HALYK_EPAY_CLIENT_SECRET=
HALYK_EPAY_SUCCESS_URL=
HALYK_EPAY_FAILURE_URL=
HALYK_EPAY_WEBHOOK_SECRET=
```

## Freedom Pay

Use a hosted checkout page and verify result callbacks before granting access.

Env:

```text
FREEDOM_PAY_ENABLED=false
FREEDOM_PAY_TEST_MODE=true
FREEDOM_PAY_MERCHANT_ID=
FREEDOM_PAY_SECRET_KEY=
FREEDOM_PAY_RESULT_URL=
FREEDOM_PAY_SUCCESS_URL=
FREEDOM_PAY_FAILURE_URL=
```

## Kaspi

Do not assume a public API shape. Configure only an official or confirmed provider integration with invoice/QR/webhook support.

Env:

```text
KASPI_ENABLED=false
KASPI_PROVIDER=official|aipay|pay_aibot|manual
KASPI_API_URL=
KASPI_API_KEY=
KASPI_WEBHOOK_SECRET=
```

If Kaspi is not configured, UI should show:

```text
Kaspi Pay пока не подключён. Используйте Telegram Stars или карту.
```

## AiPay

AiPay is supported as a customer-checklist compatibility adapter for external KZT checkout. It is disabled by default and must not be used inside Telegram as the primary digital-goods flow; Telegram Stars stays primary there.

Env:

```text
PAYMENTS_ENABLE_AIPAY=false
AIPAY_ENABLED=false
AIPAY_TEST_MODE=true
AIPAY_API_URL=
AIPAY_SECRET=
AIPAY_SUCCESS_URL=
AIPAY_FAILURE_URL=
AIPAY_CALLBACK_URL=
NEXT_PUBLIC_PAYMENTS_ENABLE_AIPAY=false
```

Endpoints:

```text
POST /api/payment/create
POST /api/payment/webhook
POST /api/payments/webhooks/aipay
```

Rules:

- Create only hosted checkout links.
- Never store card data.
- Verify `x-aipay-signature` before marking an order paid.
- Validate amount and currency against the internal order.
- Grant entitlement only after a signed webhook/status says paid.

## Crypto

Crypto is disabled by default and must use a regulated external payment provider.

No self-custody wallet, no private keys, no manual screenshot confirmation.

Env:

```text
CRYPTO_ENABLED=false
CRYPTO_PROVIDER=
CRYPTO_API_KEY=
CRYPTO_WEBHOOK_SECRET=
CRYPTO_ALLOWED_ASSETS=USDT,TON
CRYPTO_NETWORKS=TON,TRC20
```

## Webhook security

- Verify signatures where available.
- Validate provider amount and currency.
- Store raw payloads for audit.
- Process idempotently by provider event id.
- Do not expose raw sensitive payloads to regular users.
