from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# class Customer(Base):
#     __tablename__ = "customers"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)

#     orders = relationship("Order", back_populates="customer")

# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True, index=True)
#     customer_id = Column(Integer, ForeignKey("customers.id"))

#     customer = relationship("Customer", back_populates="orders")
#     items = relationship("OrderItem", back_populates="order")

# class OrderItem(Base):
#     __tablename__ = "order_items"

#     id = Column(Integer, primary_key=True, index=True)
#     product_name = Column(String, index=True)
#     order_id = Column(Integer, ForeignKey("orders.id"))

#     order = relationship("Order", back_populates="items")