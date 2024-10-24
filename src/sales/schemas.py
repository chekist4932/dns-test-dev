from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    city_name: str


class CityCreate(CityBase):
    ...


class CityModel(CityBase):
    city_id: int

    class Config:
        from_attributes = True


class StoreModel(BaseModel):
    id: int
    name: str
    city_id: int


class ProductBase(BaseModel):
    product_name: str
    price: float


class ProductCreate(ProductBase):
    ...


class ProductModel(ProductBase):
    product_id: int

    class Config:
        from_attributes = True


class SaleModel(BaseModel):
    id: int
    operation_uid: int
    sale_date: datetime
    quantity: int
    total_price: float
    store_id: int
    product_id: int


class SaleFilterParams(BaseModel):
    operation_uid: Optional[int] | None = None
    city_name: Optional[str] = None
    store_name: Optional[str] = None
    product_name: Optional[str] = None
    days_before: Optional[int] = None
    sum_above: Optional[int] = None
    sum_below: Optional[int] = None
    quantity_above: Optional[int] = None
    quantity_below: Optional[int] = None


class SaleItem(BaseModel):
    sale_id: int
    operation_uid: int
    sale_date: datetime
    quantity: int
    total_price: float
    product_name: str
    store_name: str
    city_name: str
