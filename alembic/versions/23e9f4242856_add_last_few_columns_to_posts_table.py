"""add last few columns to posts table

Revision ID: 23e9f4242856
Revises: 1b9f4d98992c
Create Date: 2026-11-08 13:13:59.683326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23e9f4242856'
down_revision: Union[str, Sequence[str], None] = '1b9f4d98992c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))  # adding a new column 'published' to the 'posts' table, it is of type Boolean and cannot be null, default value is TRUE
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))  # adding a new column 'created_at'
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')  # dropping the 'published' column from the 'posts' table, this will remove the column from the table
    op.drop_column('posts', 'created_at')  # dropping the 'created_at'
    pass
