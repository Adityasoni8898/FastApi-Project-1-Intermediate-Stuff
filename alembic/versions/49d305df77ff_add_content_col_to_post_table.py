"""add content col to post table

Revision ID: 49d305df77ff
Revises: 948517590450
Create Date: 2024-12-22 03:26:38.426717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49d305df77ff'
down_revision: Union[str, None] = '948517590450'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass