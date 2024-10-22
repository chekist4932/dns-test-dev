import datetime

from sqlalchemy import MetaData, Table, Column, Integer, Float, String, ForeignKey, DateTime

metadata = MetaData()

city = Table(
    'city',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False)
)

store = Table(
    'store',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('city_id', Integer, ForeignKey('city.id'))

)

product = Table(
    'product',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('price', Float(precision=32, decimal_return_scale=2), nullable=False)
)

sale = Table(
    'sale',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('store_id', Integer, ForeignKey('store.id')),
    Column('total_amount', Float(precision=32, decimal_return_scale=2), nullable=False),
    Column('sale_date', DateTime, default=datetime.datetime.now(datetime.UTC))
)

sale_product = Table('SaleProduct',
                     metadata,
                     Column('product_id', Integer, ForeignKey('product.id')),
                     Column('sale_id', Integer, ForeignKey('sale.id')),
                     Column('quantity', Integer, nullable=True),
                     Column('total_price', Float(precision=32, decimal_return_scale=2), nullable=False)
                     )
