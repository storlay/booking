"""update facilities title unique

Revision ID: 0c24c56fd0c4
Revises: b51f6532e29e
Create Date: 2025-06-10 11:58:42.344953

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c24c56fd0c4"
down_revision: Union[str, None] = "b51f6532e29e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "facilities", ["title"])


def downgrade() -> None:
    op.drop_constraint(None, "facilities", type_="unique")
