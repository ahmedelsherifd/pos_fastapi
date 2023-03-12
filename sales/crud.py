from .models import Customer
from sqlalchemy.orm import Session


def create_customer(db, **data):
    customer = Customer(**data)
    db.add(customer)
    db.commit()
    return customer


def create_product():
    pass


def create_order():
    pass


def get_customers():
    pass


def get_products():
    pass
