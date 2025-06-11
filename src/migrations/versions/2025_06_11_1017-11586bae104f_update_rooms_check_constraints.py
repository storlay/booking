"""update rooms check constraints

Revision ID: 11586bae104f
Revises: 0c24c56fd0c4
Create Date: 2025-06-11 10:17:47.355994

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "11586bae104f"
down_revision: Union[str, None] = "0c24c56fd0c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_room_quantity",
        "rooms",
        "quantity >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "check_room_quantity",
        "rooms",
        type_="check",
    )
