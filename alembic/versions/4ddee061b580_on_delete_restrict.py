"""on_delete_restrict

Revision ID: 4ddee061b580
Revises: 012815e29161
Create Date: 2024-10-25 00:00:26.724486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ddee061b580'
down_revision: Union[str, None] = '012815e29161'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('sale_product_id_fkey', 'sale', type_='foreignkey')
    op.drop_constraint('sale_store_id_fkey', 'sale', type_='foreignkey')
    op.create_foreign_key(None, 'sale', 'product', ['product_id'], ['product_id'], ondelete='RESTRICT')
    op.create_foreign_key(None, 'sale', 'store', ['store_id'], ['store_id'], ondelete='RESTRICT')
    op.drop_constraint('store_city_id_fkey', 'store', type_='foreignkey')
    op.create_foreign_key(None, 'store', 'city', ['city_id'], ['city_id'], ondelete='RESTRICT')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'store', type_='foreignkey')
    op.create_foreign_key('store_city_id_fkey', 'store', 'city', ['city_id'], ['city_id'])
    op.drop_constraint(None, 'sale', type_='foreignkey')
    op.drop_constraint(None, 'sale', type_='foreignkey')
    op.create_foreign_key('sale_store_id_fkey', 'sale', 'store', ['store_id'], ['store_id'])
    op.create_foreign_key('sale_product_id_fkey', 'sale', 'product', ['product_id'], ['product_id'])
    # ### end Alembic commands ###