"""add_unique_constant_store

Revision ID: e62997240983
Revises: bbd3d32693a4
Create Date: 2024-10-27 12:44:01.925419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e62997240983'
down_revision: Union[str, None] = 'bbd3d32693a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'store', ['store_name', 'city_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'store', type_='unique')
    # ### end Alembic commands ###
