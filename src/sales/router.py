from typing import Annotated, Mapping

from fastapi import APIRouter, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession

from src.sales.services import get_city_by_id, get_sales_by_params
from src.sales.schemas import SaleFilterParams, SaleItem
from src.database import get_async_session

router = APIRouter(prefix='/api', tags=['sales'])


@router.get('/city/{city_id}')
async def get_city(city_id: int, session: AsyncSession = Depends(get_async_session)):
    city = await get_city_by_id(city_id, session)
    return {'message': city}


@router.get('/sales/', response_model=list[SaleItem])
async def get_sale(filter_params: Annotated[SaleFilterParams, Query()],
                   session: AsyncSession = Depends(get_async_session)):
    sales = await get_sales_by_params(filter_params, session)
    return sales
