"""add name to users

Revision ID: 4e356ddd7b57
Revises: 2b95e644cb69
Create Date: 2025-06-01 11:07:02.460288

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4e356ddd7b57"
down_revision: Union[str, None] = "2b95e644cb69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("first_name", sa.String(length=200), nullable=True)
    )
    op.add_column("users", sa.Column("last_name", sa.String(length=200), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
