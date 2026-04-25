"""init

Revision ID: 0001
Revises:
Create Date: 2026-04-25
"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('telegram_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=255)),
        sa.Column('last_name', sa.String(length=255)),
        sa.Column('username', sa.String(length=255)),
        sa.Column('language_code', sa.String(length=16)),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
        sa.UniqueConstraint('telegram_id')
    )


def downgrade() -> None:
    op.drop_table('users')
