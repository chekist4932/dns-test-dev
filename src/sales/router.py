from typing import Annotated

from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.sales.services import get_city_by_id, get_sales_by_params, create_product, create_city, update_city_by_id, \
    delete_city_by_id, get_product_by_id, update_product_by_id, delete_product_by_id
from src.sales.schemas import SaleFilterParams, SaleItem, ProductCreate, CityCreate
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
async def create_new_product(product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    return await create_product(product, session)


@router.get('/product/{product_id}')
async def get_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await get_product_by_id(product_id, session)


@router.put("/product/{product_id}")
async def update_city(product_id: int, product_data: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    return await update_product_by_id(product_id, product_data, session)


@router.delete("/product/{product_id}")
async def update_city(product_id: int, session: AsyncSession = Depends(get_async_session)):
    return await delete_product_by_id(product_id, session)


@router.get('/sales/', response_model=list[SaleItem])
async def get_sale(filter_params: Annotated[SaleFilterParams, Query()],
                   session: AsyncSession = Depends(get_async_session)):
    return await get_sales_by_params(filter_params, session)
