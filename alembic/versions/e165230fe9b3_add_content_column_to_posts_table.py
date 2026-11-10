"""add content column to posts table

Revision ID: e165230fe9b3
Revises: 2610342ce94f
Create Date: 2026-11-08 12:46:23.490224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e165230fe9b3'
down_revision: Union[str, Sequence[str], None] = '2610342ce94f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))  # adding a new column 'content' to the 'posts' table, it is of type String and cannot be null
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')  # dropping the 'content' column from the 'posts' table, this will remove the column from the table
    pass
