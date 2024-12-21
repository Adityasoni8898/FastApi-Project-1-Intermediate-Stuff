"""remaining post cols

Revision ID: abc71d12f2c8
Revises: 91719b1375b0
Create Date: 2024-12-22 03:42:13.721114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc71d12f2c8'
down_revision: Union[str, None] = '91719b1375b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                   sa.Column("published", sa.Boolean(), nullable=False, server_default="True"))
    
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
