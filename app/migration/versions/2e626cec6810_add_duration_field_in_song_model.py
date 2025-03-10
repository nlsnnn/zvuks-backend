"""add duration field in song model

Revision ID: 2e626cec6810
Revises: e10bcfd87f98
Create Date: 2025-03-10 12:57:27.330743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e626cec6810'
down_revision: Union[str, None] = 'e10bcfd87f98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('duration', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('songs', 'duration')
    # ### end Alembic commands ###
