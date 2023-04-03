from pydantic import BaseModel, validator
from sqlalchemy import select
from starlette_context import context

from . import models
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase as Base


class CustomerInput(BaseModel):
    name: str


class CategoryInput(BaseModel):
    name: str


class ProductVariantInput(BaseModel):
    name: str
    price: Decimal


class ProductInput(BaseModel):
    name: str
    variants: list[ProductVariantInput]


class PaymentInput(BaseModel):
    amount: Decimal


class OrderItemInput(BaseModel):
    product: int
    quantity: int = 1

    _normalize_product = validator('product', allow_reuse=True)(
        models.ProductVariant.from_id)


class OrderInput(BaseModel):
    customer: int = None
    items: list[OrderItemInput]
    payment: PaymentInput

    # _normalize_items = validator('items',
    #                              allow_reuse=True)(models.OrderItem.from_list)


class Customer(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ProductVariant(BaseModel):
    id: int
    name: str
    price: Decimal

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class OrderItem(BaseModel):
    id: int
    product: ProductVariant
    quantity: int

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    customer: Customer | None
    items: list[OrderItem]

    class Config:
        orm_mode = True
