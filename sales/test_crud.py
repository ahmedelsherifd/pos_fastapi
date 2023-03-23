from .crud import create_customer, create_product, create_order, get_customers, get_variants, get_order
from app.database import Base, SessionLocal, engine
from . import models
import pytest


def test_pos_create_order(db):
    # setup

    customer_input = {"name": "Ahmed ELsherif"}

    customer = create_customer(db, **customer_input)

    product_1_input = {
        "name": "Iphone 6",
        "variants": [{
            "price": 10,
            "name": "Iphone 12 128GB",
        }]
    }
    product_2_input = {
        "name": "Iphone 12",
        "variants": [{
            "price": 20,
            "name": "Iphone 12 128GB",
        }]
    }

    create_product(db, **product_1_input)
    create_product(db, **product_2_input)
    # test crud functions that should work in POS
    customer = get_customers(db)[0]
    varinats = get_variants(db)

    variant_1 = varinats[0]
    variant_2 = varinats[1]

    order_input = {
        "customer":
        customer,
        "items": [{
            "product": variant_1,
            "quantity": 1
        }, {
            "product": variant_2,
            "quantity": 1
        }],
        "payment": {
            "amount": 30
        }
    }

    order = create_order(db, **order_input)

    assert order.id is not None
    assert order.total_price == 30
    assert order.payment.amount == 30


def test_search_customer_by_name(db):
    customer_input = {"name": "Khalaf Eldahsoury Khalaf"}
    create_customer(db, **customer_input)
    customer_input = {"name": "Reda Elmesery"}
    create_customer(db, **customer_input)

    customers = get_customers(db, search="Reda")

    assert customers[0].name == "Reda Elmesery"


def test_search_product_by_sku(db):
    product_1_input = {
        "name": "Iphone 6",
        "variants": [{
            "price": 10,
            "name": "Iphone 6 128GB",
            "SKU": "4578"
        }]
    }
    product_2_input = {
        "name": "Iphone 12",
        "variants": [{
            "price": 20,
            "name": "Iphone 12 128GB",
            "SKU": "4589"
        }]
    }
    create_product(db, **product_1_input)
    create_product(db, **product_2_input)

    products = get_variants(db, search="458")
    assert products[0].name == "Iphone 12 128GB"
