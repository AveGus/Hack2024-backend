"""empty message

Revision ID: 2887c72aed89
Revises: c7f5431c0ab3, fa484abce929
Create Date: 2024-10-04 16:22:04.032559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2887c72aed89'
down_revision: Union[str, None] = ('c7f5431c0ab3', 'fa484abce929')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
