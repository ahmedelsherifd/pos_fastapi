from datetime import datetime

from sqlalchemy.orm import Session

from .crud import (create_category, create_customer, create_product,
                   get_categories, get_variants, create_order)

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


def create_order_1(db):
    product_1 = get_variants(db, search="Honda CRV 2023 Grey")[0]
    product_2 = get_variants(db, search="Iphone 12 128GB")[0]
    data = {
        "items": [
            {
                "product": product_1,
                "quantity": 1,
                "created_at": datetime(2023, 3, 28)
            },
            {
                "product": product_2,
                "quantity": 1,
                "created_at": datetime(2023, 3, 28)
            },
        ],
        "payment": {
            "amount": 100,
            "created_at": datetime(2023, 3, 28)
        }
    }
    create_order(db, **data)


def create_order_2(db):
    product = get_variants(db, search="Iphone 12 128GB")[0]
    data = {
        "items": [{
            "product": product,
            "quantity": 1,
            "created_at": datetime(2023, 3, 29)
        }],
        "payment": {
            "amount": 20,
            "created_at": datetime(2023, 3, 29)
        }
    }
    create_order(db, **data)


def create_user_1(db):
    data = {
        "username": "leader",
        "email": "gleader21@gmail.com",
        "password": "642*A531"
    }
    crud.create_user(db, **data)


def load_data(db: Session):
    create_customer_1(db)
    create_customer_2(db)

    create_category_1(db)
    create_category_2(db)

    create_product_1(db)
    create_product_2(db)

    create_order_1(db)
    create_order_2(db)

    create_user_1(db)
    # don't use product_2 used in test_sales_by_items - order
    # don't use mar_29 as created_at in order.items used in test_sales_by_items - order
    # don't use mar_29 or mar_28 used in test_total_payments - payment