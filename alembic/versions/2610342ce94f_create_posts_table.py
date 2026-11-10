"""create posts table

Revision ID: 2610342ce94f
Revises: 
Create Date: 2026-11-08 12:34:55.629369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2610342ce94f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#   Used for upgrading the database schema, if we want to make changes to the database schema, we can use the upgrade function to create the posts table in the database
def upgrade() -> None:

    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')))

    pass

# Used for downgrading the database schema, if we want to revert the changes made by the upgrade function, we can use the downgrade function to drop the posts table from the database
def downgrade() -> None:
    op.drop_table('posts')  # dropping the posts table from the database, this will remove the table from the database
    pass
