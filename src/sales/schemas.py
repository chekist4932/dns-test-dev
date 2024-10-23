from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str


class Store(BaseModel):
    id: int
    name: str
    city_id: int


class Product(BaseModel):
    id: int
    name: str
    price: int


class Sale(BaseModel):
    id: int
    operation_uid: int
    sale_date: datetime
    quantity: int
    total_price: float
    store_id: int
    product_id: int


class SaleFilterParams(BaseModel):
    operation_uid: Optional[int] = None
    city_name: Optional[str] = None
    store_name: Optional[str] = None
    product_name: Optional[str] = None
    days_before: Optional[int] = None
    sum_above: Optional[int] = None
    sum_below: Optional[int] = None
    quantity_above: Optional[int] = None
    quantity_below: Optional[int] = None
