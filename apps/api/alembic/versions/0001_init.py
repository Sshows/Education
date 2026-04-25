"""init

Revision ID: 0001
Revises:
Create Date: 2026-04-25
"""

from alembic import op

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    from app.db.base import Base
    from app.models import models  # noqa: F401

    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    from app.db.base import Base
    from app.models import models  # noqa: F401

    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
