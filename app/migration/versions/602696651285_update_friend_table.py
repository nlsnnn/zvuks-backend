"""update friend table

Revision ID: 602696651285
Revises: 795284606b52
Create Date: 2025-02-19 13:21:37.846250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '602696651285'
down_revision: Union[str, None] = '795284606b52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
