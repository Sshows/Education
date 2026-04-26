"""payments

Revision ID: 0002_payments
Revises: 0001
Create Date: 2026-04-26
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_payments"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "payment_products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title_ru", sa.String(length=255), nullable=False),
        sa.Column("title_kk", sa.String(length=255), nullable=True),
        sa.Column("title_en", sa.String(length=255), nullable=True),
        sa.Column("description_ru", sa.Text(), nullable=True),
        sa.Column("product_type", sa.String(length=32), nullable=False),
        sa.Column("stars_price", sa.Integer(), nullable=True),
        sa.Column("kzt_price", sa.Integer(), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="XTR"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("features_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
        sa.UniqueConstraint("code"),
    )
    op.create_index("ix_payment_products_code", "payment_products", ["code"])

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("payment_products.id"), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("provider_order_id", sa.String(length=255), nullable=True),
        sa.Column("provider_payment_id", sa.String(length=255), nullable=True),
        sa.Column("checkout_url", sa.String(length=1024), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("paid_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_orders_telegram_id", "orders", ["telegram_id"])
    op.create_index("ix_orders_status", "orders", ["status"])
    op.create_index("ix_orders_provider", "orders", ["provider"])
    op.create_index("ix_orders_idempotency_key", "orders", ["idempotency_key"])

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("provider_payment_id", sa.String(length=255), nullable=True),
        sa.Column("provider_charge_id", sa.String(length=255), nullable=True),
        sa.Column("raw_payload_json", sa.JSON(), nullable=False),
        sa.Column("signature_valid", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime()),
    )
    op.create_index("ix_payments_order_id", "payments", ["order_id"])

    op.create_table(
        "entitlements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True),
        sa.Column("product_code", sa.String(length=64), nullable=False),
        sa.Column("access_type", sa.String(length=32), nullable=False),
        sa.Column("credits_total", sa.Integer(), nullable=True),
        sa.Column("credits_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("starts_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("source_order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("updated_at", sa.DateTime()),
        sa.UniqueConstraint("source_order_id"),
    )
    op.create_index("ix_entitlements_telegram_id", "entitlements", ["telegram_id"])
    op.create_index("ix_entitlements_product_code", "entitlements", ["product_code"])

    op.create_table(
        "payment_webhook_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("provider_event_id", sa.String(length=255), nullable=True),
        sa.Column("signature_valid", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("processed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("raw_payload_json", sa.JSON(), nullable=False),
        sa.Column("received_at", sa.DateTime(), nullable=False),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
    )
    op.create_index("ix_payment_webhook_events_provider", "payment_webhook_events", ["provider"])
    op.create_index("ix_payment_webhook_events_provider_event_id", "payment_webhook_events", ["provider_event_id"])
    op.create_index(
        "ix_payment_webhook_events_provider_event",
        "payment_webhook_events",
        ["provider", "provider_event_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_payment_webhook_events_provider_event", table_name="payment_webhook_events")
    op.drop_index("ix_payment_webhook_events_provider_event_id", table_name="payment_webhook_events")
    op.drop_index("ix_payment_webhook_events_provider", table_name="payment_webhook_events")
    op.drop_table("payment_webhook_events")
    op.drop_index("ix_entitlements_product_code", table_name="entitlements")
    op.drop_index("ix_entitlements_telegram_id", table_name="entitlements")
    op.drop_table("entitlements")
    op.drop_index("ix_payments_order_id", table_name="payments")
    op.drop_table("payments")
    op.drop_index("ix_orders_idempotency_key", table_name="orders")
    op.drop_index("ix_orders_provider", table_name="orders")
    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_index("ix_orders_telegram_id", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_payment_products_code", table_name="payment_products")
    op.drop_table("payment_products")
