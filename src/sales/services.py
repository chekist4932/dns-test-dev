from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.sales.models import city as city_table, sale as sale_table, store as store_table, product as product_table
from src.sales.schemas import City, SaleFilterParams


async def get_city_by_id(city_id: int, session: AsyncSession) -> City or None:
    query = select(city_table).where(city_table.c.id == city_id)
    result = await session.execute(query)
    result = result.mappings().first()

    if result is not None:
        result = City(**result)
        return result


async def get_sales_by_params(filters: SaleFilterParams, session: AsyncSession):
    query = select(sale_table,
                   product_table,
                   store_table,
                   city_table).join(product_table).join(store_table).join(city_table)

    if filters.city_name:
        query = query.filter(city_table.c.city_name == filters.city_name)

    if filters.store_name:
        query = query.filter(store_table.c.store_name == filters.store_name)

    if filters.product_name:
        query = query.filter((product_table.c.product_name == filters.product_name))

    result = await session.execute(query)
    return result.mappings().all()
