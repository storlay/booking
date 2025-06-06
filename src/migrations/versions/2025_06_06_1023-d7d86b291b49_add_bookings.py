"""add bookings

Revision ID: d7d86b291b49
Revises: 25449f6f33d6
Create Date: 2025-06-06 10:23:56.155795

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d7d86b291b49"
down_revision: Union[str, None] = "25449f6f33d6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price_per_day", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.CheckConstraint("date_to >= date_from", name="check_booking_date"),
        sa.CheckConstraint("price_per_day >= 0", name="check_booking_price"),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("bookings")
