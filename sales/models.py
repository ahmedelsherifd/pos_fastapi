from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product:
    pass


class ProductVariant:
    # with product
    pass


class Attribute:
    pass


class AttributeOption:
    pass


class ProductVariantDetail:
    # with AttributeOption
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)


class Order:
    pass


class OrderItem:
    pass