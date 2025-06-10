"""add facilities

Revision ID: b51f6532e29e
Revises: 18ec03fe66c0
Create Date: 2025-06-10 11:45:36.095360

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b51f6532e29e"
down_revision: Union[str, None] = "18ec03fe66c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id", "facility_id", name="uq_room_facility"),
    )


def downgrade() -> None:
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
