from .models import Customer, Product, ProductVariant, OrderItem, Order, Payement, Category, User

from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from app.database import engine
from datetime import datetime
from sqlalchemy import or_


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
    total_price = sum([item.subtotal_price for item in items])
    order = Order(**data,
                  items=items,
                  payment=payment,
                  total_price=total_price)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_product(db: Session, pk: int):
    stmt = select(Product).where(Product.id == pk)
    result = db.scalars(stmt).one()
    return result


def get_customer(db: Session, pk: int):
    stmt = select(Customer).where(Customer.id == pk)
    result = db.scalars(stmt).one()
    return result


def get_order(db: Session, id: int):
    stmt = select(Order).where(Order.id == id)
    result = db.scalars(stmt).one()
    return result


def get_customers(db: Session, search: str = None):
    stmt = select(Customer)
    if search:
        stmt = stmt.where(Customer.name.contains(search))
    result = db.scalars(stmt).all()
    return result


def get_variants(db: Session, search: str = None, category: int = None):
    stmt = select(ProductVariant)

    if category:
        stmt = stmt.join(
            ProductVariant.product).where(Product.category_id == category)
    if search:
        stmt = stmt.where(
            or_(ProductVariant.SKU.startswith(search),
                ProductVariant.name.contains(search)))

    result = db.scalars(stmt).all()
    return result


def create_category(db: Session, **data):
    category = Category(**data)
    db.add(category)
    db.commit()
    return category


def get_categories(db: Session, search: str = None):
    stmt = select(Category)
    if search:
        stmt = stmt.where(Category.name.contains(search))
    result = db.scalars(stmt).all()
    return result


def get_sales_by_items(db: Session,
                       search: str = None,
                       start_date: datetime = None,
                       end_date: datetime = None):
    stmt = select(ProductVariant,
                  func.sum(OrderItem.quantity).label("total_quantity"),
                  func.sum(
                      OrderItem.subtotal_price).label("total_sales")).join(
                          ProductVariant.orders)
    if start_date:
        stmt = stmt.filter(OrderItem.created_at >= start_date)
    if end_date:
        stmt = stmt.filter(OrderItem.created_at <= end_date)

    if search:
        stmt = stmt.where(ProductVariant.name.contains(search))

    stmt = stmt.group_by(OrderItem.product_id)

    result = db.execute(stmt).all()

    return result


def get_total_payments_node(db: Session,
                            start_date: datetime = None,
                            end_date: datetime = None):
    stmt = select(func.sum(Payement.amount))
    if start_date:
        stmt = stmt.filter(Payement.created_at >= start_date)
    if end_date:
        stmt = stmt.filter(Payement.created_at <= end_date)

    result = db.execute(stmt).scalar()

    return result


def get_total_payments(db: Session,
                       start_date: datetime = None,
                       end_date: datetime = None):
    stmt = select(
        func.date(Payement.created_at).label("date"),
        func.sum(Payement.amount).label("total_payments")).group_by(
            func.date(Payement.created_at))

    if start_date:
        stmt = stmt.filter(Payement.created_at >= start_date)
    if end_date:
        stmt = stmt.filter(Payement.created_at <= end_date)

    result = db.execute(stmt).all()

    return result


def authenticate_user(db: Session, username: str, password: str):
    return None


def create_user(db: Session, **data):
    user = User(**data)
    db.add(user)
    db.commit()
    return user
