"""add_unique_constant_product

Revision ID: 875770926f62
Revises: e62997240983
Create Date: 2024-10-27 12:46:25.289009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '875770926f62'
down_revision: Union[str, None] = 'e62997240983'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'product', ['product_name', 'price'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='unique')
    # ### end Alembic commands ###
