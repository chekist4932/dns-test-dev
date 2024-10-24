from datetime import timedelta

from fastapi import HTTPException

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.sales.models import City as cityTable, Sale as saleTable, Store as storeTable, Product as productTable
from src.sales.schemas import CityModel, ProductModel, SaleFilterParams, ProductCreate, CityCreate


async def get_city_by_id(city_id: int, session: AsyncSession):
    city = await session.get(cityTable, city_id)
    if city is not None:
        return CityModel.from_orm(city)

    return HTTPException(status_code=404, detail="City not found")


async def create_city(city_name: str, session: AsyncSession):
    result = await session.execute(select(cityTable).where(cityTable.city_name == city_name))
    existing_city = result.scalars().first()

    if existing_city:
        return existing_city

    new_city = cityTable(city_name=city_name)
    session.add(new_city)
    await session.commit()
    await session.refresh(new_city)

    return new_city


async def update_city_by_id(city_id: int, city_data: CityCreate, session: AsyncSession):
    city = await session.get(cityTable, city_id)
    if city:
        for key, value in city_data.dict().items():
            setattr(city, key, value)
        await session.commit()

        return city
    return HTTPException(status_code=404, detail="City not found")


async def delete_city_by_id(city_id: int, session: AsyncSession):
    city = await session.get(cityTable, city_id)

    if city is not None:
        await session.delete(city)
        await session.commit()
        return CityModel.from_orm(city)

    return HTTPException(status_code=404, detail="City not found")


async def create_product(product: ProductCreate, session: AsyncSession):
    query = select(productTable).where(productTable.product_name == product.product_name,
                                       productTable.price == product.price)
    existing_product = await session.execute(query)

    if existing_product.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Product with this name and price already exists")

    new_product = productTable(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


async def get_product_by_id(product_id: int, session: AsyncSession):
    product = await session.get(productTable, product_id)
    if product is not None:
        return ProductModel.from_orm(product)

    return HTTPException(status_code=404, detail="Product not found")


async def update_product_by_id(product_id: int, product_data: ProductCreate, session: AsyncSession):
    product = await session.get(productTable, product_id)
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        await session.commit()

        return product
    return HTTPException(status_code=404, detail="Product not found")


async def delete_product_by_id(product_id: int, session: AsyncSession):
    product = await session.get(productTable, product_id)

    if product is not None:
        await session.delete(product)
        await session.commit()
        return ProductModel.from_orm(product)

    return HTTPException(status_code=404, detail="Product not found")


async def get_sales_by_params(filters: SaleFilterParams, session: AsyncSession):
    base_query = select(saleTable.sale_id,
                        saleTable.operation_uid,
                        saleTable.sale_date,
                        saleTable.quantity,
                        saleTable.total_price,
                        productTable.product_name,
                        storeTable.store_name,
                        cityTable.city_name).join(productTable).join(storeTable).join(cityTable)

    query = base_query

    if filters.city_name:
        query = query.filter(cityTable.city_name == filters.city_name)

    if filters.store_name:
        query = query.filter(storeTable.store_name == filters.store_name)

    if filters.product_name:
        query = query.filter(productTable.product_name == filters.product_name)

    if filters.days_before:
        query = query.filter(saleTable.sale_date >= func.current_timestamp() - timedelta(days=filters.days_before))

    if filters.sum_above:
        subquery = select(saleTable.operation_uid) \
            .group_by(saleTable.operation_uid) \
            .having(func.sum(saleTable.total_price) > filters.sum_above)
        query = query.filter(saleTable.operation_uid.in_(subquery))

    if filters.sum_below:
        subquery = select(saleTable.operation_uid) \
            .group_by(saleTable.operation_uid) \
            .having(func.sum(saleTable.total_price) < filters.sum_below)
        query = query.filter(saleTable.operation_uid.in_(subquery))

    if filters.quantity_above:
        subquery = select(saleTable.operation_uid) \
            .group_by(saleTable.operation_uid) \
            .having(func.sum(saleTable.quantity) > filters.quantity_above)
        query = query.filter(saleTable.operation_uid.in_(subquery))

    if filters.quantity_below:
        subquery = select(saleTable.operation_uid) \
            .group_by(saleTable.operation_uid) \
            .having(func.sum(saleTable.quantity) < filters.quantity_below).subquery()
        query = query.filter(saleTable.operation_uid.in_(subquery))

    if filters.operation_uid:
        query = query.filter(saleTable.operation_uid == filters.operation_uid)

    if query == base_query:
        return []

    result = await session.execute(query)
    return result.mappings().all()
