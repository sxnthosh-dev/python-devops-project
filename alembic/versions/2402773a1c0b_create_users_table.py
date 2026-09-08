"""create users table

Revision ID: 2402773a1c0b
Revises:
Create Date: 2026-09-02 09:51:14.101161

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2402773a1c0b"
down_revision = None
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
