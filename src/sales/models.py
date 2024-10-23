from datetime import datetime, UTC

from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, DateTime, DECIMAL

metadata = MetaData()

city = Table(
    'city',
    metadata,
    Column('city_id', Integer, primary_key=True, autoincrement=True),
    Column('city_name', String, nullable=False)
)

store = Table(
    'store',
    metadata,
    Column('store_id', Integer, primary_key=True, autoincrement=True),
    Column('store_name', String, nullable=False),
    Column('city_id', Integer, ForeignKey('city.city_id'))

)

product = Table(
    'product',
    metadata,
    Column('product_id', Integer, primary_key=True, autoincrement=True),
    Column('product_name', String, nullable=False),
    Column('price', DECIMAL(precision=10, scale=2), nullable=False)
)

sale = Table(
    'sale',
    metadata,
    Column('sale_id', Integer, primary_key=True, autoincrement=True),
    Column('operation_uid', Integer, nullable=False),
    Column('sale_date', DateTime, default=datetime.now(UTC)),
    Column('quantity', Integer, nullable=False),
    Column('total_price', DECIMAL(precision=10, scale=2), nullable=False),
    Column('store_id', Integer, ForeignKey('store.store_id')),
    Column('product_id', Integer, ForeignKey('product.product_id'))

)

# sale_product = Table('SaleProduct',
#                      metadata,
#                      Column('product_id', Integer, ForeignKey('product.id')),
#                      Column('sale_id', Integer, ForeignKey('sale.id')),
#                      Column('quantity', Integer, nullable=True),
#                      Column('total_price', DECIMAL(precision=10, scale=2), nullable=False)
#                      )
