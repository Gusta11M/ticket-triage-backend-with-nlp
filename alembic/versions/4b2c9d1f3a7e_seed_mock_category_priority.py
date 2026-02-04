"""Seed mock Category and Priority data

Revision ID: 4b2c9d1f3a7e
Revises: f81e1b6c9022
Create Date: 2026-02-04 16:45:00.000000

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4b2c9d1f3a7e"
down_revision: Union[str, Sequence[str], None] = "f81e1b6c9022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    category_table = sa.table(
        "Category",
        sa.column("id", sa.Integer),
        sa.column("category_name", sa.String),
        sa.column("description", sa.String),
        sa.column("created_at", sa.DateTime),
    )

    priority_table = sa.table(
        "Priority",
        sa.column("id", sa.Integer),
        sa.column("priority_name", sa.String),
        sa.column("level", sa.Integer),
        sa.column("created_at", sa.DateTime),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        category_table,
        [
            {"id": 1, "category_name": "Bug", "description": "Erros e crashes", "created_at": now},
            {"id": 2, "category_name": "Feature", "description": "Novas funcionalidades", "created_at": now},
            {"id": 3, "category_name": "Support", "description": "Ajuda e duvidas", "created_at": now},
        ],
    )

    op.bulk_insert(
        priority_table,
        [
            {"id": 1, "priority_name": "Low", "level": 1, "created_at": now},
            {"id": 2, "priority_name": "Medium", "level": 2, "created_at": now},
            {"id": 3, "priority_name": "High", "level": 3, "created_at": now},
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DELETE FROM "Priority" WHERE id IN (1, 2, 3)')
    op.execute('DELETE FROM "Category" WHERE id IN (1, 2, 3)')
