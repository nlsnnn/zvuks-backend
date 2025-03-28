"""delete duration field in Song model

Revision ID: fe3e91545f94
Revises: 2e626cec6810
Create Date: 2025-03-20 13:48:11.727758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe3e91545f94'
down_revision: Union[str, None] = '2e626cec6810'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('songs', 'duration')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
