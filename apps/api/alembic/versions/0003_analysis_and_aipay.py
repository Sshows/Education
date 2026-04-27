"""analysis audit and first free analysis

Revision ID: 0003_analysis_and_aipay
Revises: 0002_payments
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_analysis_and_aipay"
down_revision = "0002_payments"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("free_analysis_used", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "analyses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True),
        sa.Column("payment_id", sa.Integer(), sa.ForeignKey("payments.id"), nullable=True),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("subject_pair", sa.String(length=64), nullable=False),
        sa.Column("quota", sa.String(length=32), nullable=False, server_default="general"),
        sa.Column("specs_json", sa.JSON(), nullable=False),
        sa.Column("result_json", sa.JSON(), nullable=False),
        sa.Column("card_url", sa.String(length=1024), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_analyses_user_id", "analyses", ["user_id"])
    op.create_index("ix_analyses_telegram_id", "analyses", ["telegram_id"])
    op.create_index("ix_analyses_subject_pair", "analyses", ["subject_pair"])


def downgrade() -> None:
    op.drop_index("ix_analyses_subject_pair", table_name="analyses")
    op.drop_index("ix_analyses_telegram_id", table_name="analyses")
    op.drop_index("ix_analyses_user_id", table_name="analyses")
    op.drop_table("analyses")
    op.drop_column("users", "free_analysis_used")
