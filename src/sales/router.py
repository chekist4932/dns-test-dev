from typing import Annotated

from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.sales.services import get_city_by_id, get_sales_by_params, create_product, create_city, update_city_by_id, \
    delete_city_by_id, get_product_by_id, update_product_by_id, delete_product_by_id, get_store_by_id, create_store, \
    update_store_by_id, delete_store_by_id, get_sale_by_id, create_sale, update_sale_by_id, delete_sale_by_id

from src.sales.schemas import SaleFilterParams, ProductCreate, CityCreate, StoreCreate, SaleCreate
from src.database import get_async_session

router = APIRouter(prefix='/api', tags=['sales'])


@router.post('/city/{city_name}')
async def create_new_city(city_name: str, session: AsyncSession = Depends(get_async_session)):
    return await create_city(city_name, session)


@router.get('/city/{city_id}')
async def get_city(city_id: int, session: AsyncSession = Depends(get_async_session)):
    return await get_city_by_id(city_id, session)


@router.put("/cities/{city_id}")
async def update_city(city_id: int, city_data: CityCreate, session: AsyncSession = Depends(get_async_session)):
    return await update_city_by_id(city_id, city_data, session)


@router.delete("/cities/{city_id}")
async def delete_city(city_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_city_by_id(city_id, session)


@router.post('/product')
async def create_new_product(product_data: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    return await create_product(product_data, session)


@router.get('/product/{product_id}')
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await get_product_by_id(product_id, session)


@router.put("/product/{product_id}")
async def update_product(product_id: int, product_data: ProductCreate,
                         session: AsyncSession = Depends(get_async_session)):
    return await update_product_by_id(product_id, product_data, session)


@router.delete("/product/{product_id}")
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_product_by_id(product_id, session)


@router.post('/store')
async def create_new_store(store_data: StoreCreate, session: AsyncSession = Depends(get_async_session)):
    return await create_store(store_data, session)


@router.get('/store/{store_id}')
async def get_store(store_id: int, session: AsyncSession = Depends(get_async_session)):
    return await get_store_by_id(store_id, session)


@router.put("/store/{store_id}")
async def update_store(store_id: int, store_data: StoreCreate, session: AsyncSession = Depends(get_async_session)):
    return await update_store_by_id(store_id, store_data, session)


@router.delete("/store/{store_id}")
async def delete_store(store_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_store_by_id(store_id, session)


@router.get('/sale/{sale_id}')
async def get_sale(sale_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    return await get_sale_by_id(sale_id, session)


@router.post('/sale')
async def create_new_sale(sale_data: SaleCreate, session: AsyncSession = Depends(get_async_session)):
    return await create_sale(sale_data, session)


@router.put("/sale/{sale_id}")
async def update_sale(sale_id: int, sale_data: SaleCreate, session: AsyncSession = Depends(get_async_session)):
    return await update_sale_by_id(sale_id, sale_data, session)


@router.delete('/sale/{sale_id}')
async def delete_sale(sale_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_sale_by_id(sale_id, session)


@router.get('/sales/')
async def get_sale(filter_params: Annotated[SaleFilterParams, Query()],
                   session: AsyncSession = Depends(get_async_session)):
    return await get_sales_by_params(filter_params, session)
