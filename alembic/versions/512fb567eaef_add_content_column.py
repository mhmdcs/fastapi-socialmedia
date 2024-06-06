"""add content column

Revision ID: 512fb567eaef
Revises: ffc1cfe538fe
Create Date: 2024-06-06 19:57:19.692565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512fb567eaef'
down_revision: Union[str, None] = 'ffc1cfe538fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
