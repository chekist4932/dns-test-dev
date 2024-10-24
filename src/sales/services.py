from datetime import timedelta

from fastapi import HTTPException

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.sales.models import City as cityTable, Sale as saleTable, Store as storeTable, Product as productTable
from src.sales.schemas import CityModel, ProductModel, StoreModel, SaleFilterParams, ProductCreate, CityCreate, \
    StoreCreate


async def get_city_by_id(city_id: int, session: AsyncSession):
    city = await session.get(cityTable, city_id)
    if city:
        return CityModel.from_orm(city)

    raise HTTPException(status_code=404, detail="City not found")


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
    raise HTTPException(status_code=404, detail="City not found")


async def delete_city_by_id(city_id: int, session: AsyncSession):
    city = await session.get(cityTable, city_id)

    if city:
        await session.delete(city)
        await session.commit()
        return CityModel.from_orm(city)

    raise HTTPException(status_code=404, detail="City not found")


async def create_product(product_data: ProductCreate, session: AsyncSession):
    query = select(productTable).where(and_(productTable.product_name == product_data.product_name,
                                            productTable.price == product_data.price))
    existing_product = await session.execute(query)
    existing_product = existing_product.scalars().first()
    if existing_product:
        return existing_product

    new_product = productTable(**product_data.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


async def get_product_by_id(product_id: int, session: AsyncSession):
    product = await session.get(productTable, product_id)
    if product:
        return ProductModel.from_orm(product)

    raise HTTPException(status_code=404, detail="Product not found")


async def update_product_by_id(product_id: int, product_data: ProductCreate, session: AsyncSession):
    product = await session.get(productTable, product_id)
    if product:
        for key, value in product_data.dict().items():
            setattr(product, key, value)
        await session.commit()

        return product
    raise HTTPException(status_code=404, detail="Product not found")


async def delete_product_by_id(product_id: int, session: AsyncSession):
    product = await session.get(productTable, product_id)

    if product:
        await session.delete(product)
        await session.commit()
        return ProductModel.from_orm(product)

    raise HTTPException(status_code=404, detail="Product not found")


async def get_store_by_id(store_id: int, session: AsyncSession):
    store = await session.get(storeTable, store_id)
    if store:
        return StoreModel.from_orm(store)

    raise HTTPException(status_code=404, detail="Store not found")


async def create_store(store_data: StoreCreate, session: AsyncSession):
    query = select(storeTable).where(
        and_(storeTable.store_name == store_data.store_name, storeTable.city_id == store_data.city_id))

    result = await session.execute(query)
    store = result.scalars().first()

    if store:
        return store

    await get_city_by_id(store_data.city_id, session)

    new_store = storeTable(**store_data.model_dump())
    session.add(new_store)
    await session.commit()
    await session.refresh(new_store)

    return new_store


async def update_store_by_id(store_id: int, store_data: StoreCreate, session: AsyncSession):
    store = await session.get(storeTable, store_id)

    if store:
        await get_city_by_id(store_data.city_id, session)

        for key, value in store_data.dict().items():
            setattr(store, key, value)
        await session.commit()

        return store
    raise HTTPException(status_code=404, detail="Store not found")


async def delete_store_by_id(store_id: int, session: AsyncSession):
    store = await session.get(storeTable, store_id)

    if store:
        await session.delete(store)
        await session.commit()
        return StoreModel.from_orm(store)

    raise HTTPException(status_code=404, detail="Store not found")


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
