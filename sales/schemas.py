from pydantic import BaseModel, validator
from sqlalchemy import select

from starlette_context import context
from . import models
from decimal import Decimal


def get_object(model_klass):

    def _get_object(id):
        db = context["db"]
        stmt = select(model_klass).where(model_klass.id == id)
        result = db.scalar(stmt)
        return result

    return _get_object


class Payment(BaseModel):
    amount: Decimal


class OrderItemInput(BaseModel):
    product: int
    quantity: int = 1

    _normalize_product = validator('product', allow_reuse=True)(get_object(
        models.ProductVariant))


class OrderInput(BaseModel):
    customer: int = None
    items: list[OrderItemInput]
    payment: Payment
