"""add created_at to booking

Revision ID: 18ec03fe66c0
Revises: 2421a27bbc5d
Create Date: 2025-06-09 14:14:25.357327

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "18ec03fe66c0"
down_revision: Union[str, None] = "2421a27bbc5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("bookings", "created_at")
