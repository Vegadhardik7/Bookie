"""add review table

Revision ID: cd1ce242c386
Revises: 7bdb77e23a2f
Create Date: 2025-02-01 15:41:14.257073

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cd1ce242c386'
down_revision: Union[str, None] = '7bdb77e23a2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('review_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('user_uid', sa.Uuid(), nullable=True),
    sa.Column('book_uid', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['book_uid'], ['book.uid'], ),
    sa.ForeignKeyConstraint(['user_uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    # ### end Alembic commands ###
