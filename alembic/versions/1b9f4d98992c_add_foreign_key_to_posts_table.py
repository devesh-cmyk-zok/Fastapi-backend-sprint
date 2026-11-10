"""add foreign key to posts table

Revision ID: 1b9f4d98992c
Revises: c4bbb456ffee
Create Date: 2026-11-08 13:09:30.312948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b9f4d98992c'
down_revision: Union[str, Sequence[str], None] = 'c4bbb456ffee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))  # adding a new column 'owner_id' to the 'posts' table, it is of type Integer and cannot be null
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')

    pass
