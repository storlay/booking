"""update rooms check constrains

Revision ID: efa10ebece02
Revises: d7d86b291b49
Create Date: 2025-06-06 10:30:07.232222

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "efa10ebece02"
down_revision: Union[str, None] = "d7d86b291b49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_room_price",
        "rooms",
        "price >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "check_room_price",
        "rooms",
        type_="check",
    )
