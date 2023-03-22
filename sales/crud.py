from .models import Customer, Product, ProductVariant, OrderItem, Order, Payement
from sqlalchemy.orm import Session
from sqlalchemy import select, func


def create_customer(db: Session, **data):
    customer = Customer(**data)
    db.add(customer)
    db.commit()
    return customer


def create_product(db: Session, **data):
    variants_data = data.pop("variants", [])
    variants = [
        ProductVariant(**variant_data) for variant_data in variants_data
    ]
    product = Product(**data, variants=variants)
    db.add(product)
    db.commit()
    return product


def create_order(db: Session, **data):
    items_data = data.pop("items", [])
    unit_price = lambda item: item['product'].price
    subtotal_price = lambda item: item['quantity'] * unit_price(item)
    items = [
        OrderItem(**item_data,
                  unit_price=unit_price(item_data),
                  subtotal_price=subtotal_price(item_data))
        for item_data in items_data
    ]
    payment_data = data.pop("payment")
    payment = Payement(**payment_data)
    order = Order(**data, items=items, payment=payment)
    db.add(order)
    db.commit()
    sum_subtoal_price = db.query(func.sum(OrderItem.subtotal_price)).filter(
        OrderItem.order == order).scalar_subquery()

    order.total_price = sum_subtoal_price
    db.commit()

    db.refresh(order)

    return order


def get_customers(db: Session):
    stmt = select(Customer)
    result = db.scalars(stmt).all()
    return result


def get_variants(db: Session):
    stmt = select(ProductVariant)
    result = db.scalars(stmt).all()
    return result
