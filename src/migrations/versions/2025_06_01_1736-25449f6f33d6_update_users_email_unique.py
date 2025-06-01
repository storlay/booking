"""update users email unique

Revision ID: 25449f6f33d6
Revises: 4e356ddd7b57
Create Date: 2025-06-01 17:36:08.979265

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "25449f6f33d6"
down_revision: Union[str, None] = "4e356ddd7b57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
