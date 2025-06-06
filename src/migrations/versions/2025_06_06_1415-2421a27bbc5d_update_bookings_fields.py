"""update bookings fields

Revision ID: 2421a27bbc5d
Revises: efa10ebece02
Create Date: 2025-06-06 14:15:01.642510

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2421a27bbc5d"
down_revision: Union[str, None] = "efa10ebece02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
    )
    op.drop_column("bookings", "price_per_day")


def downgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "price_per_day",
            sa.NUMERIC(precision=10, scale=2),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("bookings", "price")
