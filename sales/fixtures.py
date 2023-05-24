from datetime import datetime

from sqlalchemy.orm import Session

from sales.crud import (create_category, create_customer, create_product,
                        get_categories, get_variants, create_order)

from app.database import SessionLocal

from . import crud


def create_customer_1(db):
    data = {"name": "Khalaf Eldahsoury Khalaf"}
    create_customer(db, **data)


def create_customer_2(db):
    data = {"name": "Reda Elmesery"}
    create_customer(db, **data)


def create_category_1(db):
    data = {"name": "Cars"}
    create_category(db, **data)


def create_category_2(db):
    data = {"name": "Phones"}
    create_category(db, **data)


def create_product_1(db):

    category = get_categories(db, search="Cars")[0]
    data = {
        "name": "Honda CRV 2023",
        "category": category,
        "variants": [{
            "price": 100,
            "name": "Honda CRV 2023 Grey",
            "SKU": "4578"
        }]
    }
    create_product(db, **data)


def create_product_2(db):
    category = get_categories(db, search="Phones")[0]
    data = {
        "name": "Iphone 12",
        "category": category,
        "variants": [{
            "price": 20,
            "name": "Iphone 12 128GB",
            "SKU": "4589"
        }]
    }
    create_product(db, **data)


def create_product_3(db):
    category = get_categories(db, search="Phones")[0]
    data = {
        "name": "Iphone 6",
        "category": category,
        "variants": [{
            "price": 20,
            "name": "Iphone 6 128GB",
            "SKU": "4579"
        }]
    }
    create_product(db, **data)


def create_user_1(db):
    data = {
        "username": "leader",
        "email": "gleader21@gmail.com",
        "password": "642*A531"
    }
    crud.create_user(db, **data)


def main():
    db = SessionLocal()
    create_category_1(db)
    create_category_2(db)
    create_product_1(db)
    create_product_2(db)
    create_product_3(db)
    create_user_1(db)