from sqlalchemy import MetaData, Table

metadata = MetaData()

product = Table(
    'product',
    metadata
)

store = Table(
    'store',
    metadata
)

city = Table(
    'city',
    metadata
)

sale = Table(
    'sale',
    metadata
)
