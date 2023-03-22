from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal

from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)

    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="product")


class ProductVariant(Base):
    # with product
    __tablename__ = "variants"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))
    # sku: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))

    product: Mapped["Product"] = relationship("Product",
                                              back_populates="variants")
    orders: Mapped[list["OrderItem"]] = relationship("OrderItem",
                                                     back_populates="product")


class Attribute:
    pass


class AttributeOption:
    pass


class VariantDetail:
    # with AttributeOption
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)

    orders: Mapped["Order"] = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer,
                                             ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship("Customer",
                                                back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem",
                                                    back_populates="order")
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10,
                                                         scale=2),
                                                 default=0)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("variants.id"))
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2),
                                                default=0)
    subtotal_price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10,
                                                            scale=2),
                                                    default=0)

    product: Mapped["ProductVariant"] = relationship("ProductVariant",
                                                     back_populates="orders")
    order: Mapped["Order"] = relationship("Order", back_populates="items")
