from datetime import timedelta

from sqlalchemy import select, func
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
    base_query = select(sale_table.c.sale_id,
                        sale_table.c.operation_uid,
                        sale_table.c.sale_date,
                        sale_table.c.quantity,
                        sale_table.c.total_price,
                        product_table.c.product_name,
                        store_table.c.store_name,
                        city_table.c.city_name).join(product_table).join(store_table).join(city_table)

    query = base_query

    if filters.city_name:
        query = query.filter(city_table.c.city_name == filters.city_name)

    if filters.store_name:
        query = query.filter(store_table.c.store_name == filters.store_name)

    if filters.product_name:
        query = query.filter((product_table.c.product_name == filters.product_name))

    if filters.days_before:
        query = query.filter(sale_table.c.sale_date >= func.current_timestamp() - timedelta(days=filters.days_before))

    if filters.sum_above:
        subquery = select(sale_table.c.operation_uid) \
            .group_by(sale_table.c.operation_uid) \
            .having(func.sum(sale_table.c.total_price) > filters.sum_above).subquery()
        query = query.filter(sale_table.c.operation_uid.in_(subquery))

    if filters.sum_below:
        subquery = select(sale_table.c.operation_uid) \
            .group_by(sale_table.c.operation_uid) \
            .having(func.sum(sale_table.c.total_price) < filters.sum_below).subquery()
        query = query.filter(sale_table.c.operation_uid.in_(subquery))

    if filters.quantity_above:
        subquery = select(sale_table.c.operation_uid) \
            .group_by(sale_table.c.operation_uid) \
            .having(func.sum(sale_table.c.quantity) > filters.quantity_above).subquery()
        query = query.filter(sale_table.c.operation_uid.in_(subquery))

    if filters.quantity_below:
        subquery = select(sale_table.c.operation_uid) \
            .group_by(sale_table.c.operation_uid) \
            .having(func.sum(sale_table.c.quantity) < filters.quantity_below).subquery()
        query = query.filter(sale_table.c.operation_uid.in_(subquery))

    if filters.operation_uid:
        query = query.filter(sale_table.c.operation_uid == filters.operation_uid)

    if query == base_query:
        return []

    result = await session.execute(query)
    return result.mappings().all()
