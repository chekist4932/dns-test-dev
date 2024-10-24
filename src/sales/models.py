from datetime import datetime, UTC

from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()


Base = declarative_base(metadata=metadata)


class City(Base):
    __tablename__ = 'city'

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String, nullable=False)


class Store(Base):
    __tablename__ = 'store'

    store_id = Column(Integer, primary_key=True, autoincrement=True)
    store_name = Column(String, nullable=False)

    city_id = Column(Integer, ForeignKey('city.city_id'))


class Product(Base):
    __tablename__ = 'product'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    price = Column(DECIMAL(precision=10, scale=2), nullable=False)


class Sale(Base):
    __tablename__ = 'sale'

    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    operation_uid = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.now(UTC))
    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(precision=10, scale=2), nullable=False)

    store_id = Column(Integer, ForeignKey('store.store_id'))
    product_id = Column(Integer, ForeignKey('product.product_id'))

#
# City = Table(
#     'city',
#     metadata,
#     Column('city_id', Integer, primary_key=True, autoincrement=True),
#     Column('city_name', String, nullable=False)
# )
#
# Store = Table(
#     'store',
#     metadata,
#     Column('store_id', Integer, primary_key=True, autoincrement=True),
#     Column('store_name', String, nullable=False),
#     Column('city_id', Integer, ForeignKey('city.city_id'))
#
# )
#
# Product = Table(
#     'product',
#     metadata,
#     Column('product_id', Integer, primary_key=True, autoincrement=True),
#     Column('product_name', String, nullable=False),
#     Column('price', DECIMAL(precision=10, scale=2), nullable=False)
# )
#
# Sale = Table(
#     'sale',
#     metadata,
#     Column('sale_id', Integer, primary_key=True, autoincrement=True),
#     Column('operation_uid', Integer, nullable=False),
#     Column('sale_date', DateTime, default=datetime.now(UTC)),
#     Column('quantity', Integer, nullable=False),
#     Column('total_price', DECIMAL(precision=10, scale=2), nullable=False),
#     Column('store_id', Integer, ForeignKey('store.store_id')),
#     Column('product_id', Integer, ForeignKey('product.product_id'))
# )

# sale_product = Table('SaleProduct',
#                      metadata,
#                      Column('product_id', Integer, ForeignKey('product.id')),
#                      Column('sale_id', Integer, ForeignKey('sale.id')),
#                      Column('quantity', Integer, nullable=True),
#                      Column('total_price', DECIMAL(precision=10, scale=2), nullable=False)
#                      )
