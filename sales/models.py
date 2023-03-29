from datetime import datetime
from decimal import Decimal

from sqlalchemy import (DECIMAL, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"),
                                             nullable=True)

    variants: Mapped[list["ProductVariant"]] = relationship(
        back_populates="product")
    category: Mapped["Category"] = relationship(back_populates="products")


class ProductVariant(Base):
    # with product
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    SKU: Mapped[str] = mapped_column(nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship(back_populates="variants")
    orders: Mapped[list["OrderItem"]] = relationship(back_populates="product")


class Attribute:
    pass


class AttributeOption:
    pass


class VariantDetail:
    # with AttributeOption
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)

    orders: Mapped["Order"] = relationship(back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"),
                                             nullable=True)
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10,
                                                         scale=2),
                                                 default=0)
    payment: Mapped["Payement"] = relationship(back_populates="order")


class Payement(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    amount: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2),
                                            default=0)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True),
                                          server_default=func.now())
    order: Mapped["Order"] = relationship(back_populates="payment")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("variants.id"))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2),
                                                default=0)
    subtotal_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10,
                                                            scale=2),
                                                    default=0)

    created_at: Mapped[datetime] = Column(DateTime(timezone=True),
                                          server_default=func.now())
    product: Mapped["ProductVariant"] = relationship(back_populates="orders")
    order: Mapped["Order"] = relationship(back_populates="items")
