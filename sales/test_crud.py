import pytest

from . import models
from .crud import (create_category, create_customer, create_order,
                   create_product, get_customers, get_order,
                   get_sales_by_items, get_variants, get_total_payments_node,
                   get_total_payments, get_categories)

from . import crud
from datetime import datetime
from .somedata import load_data


def test_pos_create_order(db):
    # setup

    customer_input = {"name": "Ahmed ELsherif"}

    customer = create_customer(db, **customer_input)

    product_1_input = {
        "name": "Iphone 6",
        "variants": [{
            "price": 10,
            "name": "Iphone 6 128GB",
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
    load_data(db)
    customers = get_customers(db, search="Reda")

    assert customers[0].name == "Reda Elmesery"


def test_search_product_by_sku(db):
    load_data(db)
    products = get_variants(db, search="458")
    assert products[0].name == "Iphone 12 128GB"


def test_filter_product_by_catgory(db):
    load_data(db)
    phones_cat = get_categories(db, search="Phones")[0]
    products = get_variants(db, category=phones_cat.id)
    assert products[0].name == "Iphone 12 128GB"
    assert len(products) == 1


def test_sales_by_items(db):
    load_data(db)

    item = get_sales_by_items(db, search="Iphone 12 128GB")[0]

    assert item.total_sales == 40
    assert item.total_quantity == 2


def test_sales_by_items_filter_by_date(db):
    load_data(db)

    start_date = datetime(2023, 3, 29)
    end_date = datetime(2023, 3, 29)
    mar_29 = get_sales_by_items(db, start_date=start_date,
                                end_date=end_date)[0]

    assert mar_29.total_sales == 20
    assert mar_29.total_quantity == 1


def test_total_payments(db):
    load_data(db)

    start_date = datetime(2023, 3, 29)
    end_date = datetime(2023, 3, 29)
    total_payments = get_total_payments_node(db,
                                             start_date=start_date,
                                             end_date=end_date)
    assert total_payments == 20


def test_total_payments_daily(db):
    load_data(db)

    total_payments = get_total_payments(db)
    mar_28 = total_payments[0]
    mar_29 = total_payments[1]
    assert mar_28.date == "2023-03-28"
    assert mar_28.total_payments == 100
    assert mar_29.total_payments == 20


def test_create_user(db):
    data = {
        "username": "gleader21",
        "email": "gleader21@gmail.com",
        "password": "642@A531"
    }
    crud.create_user(db, **data)


def test_authenticate_user(db):
    data = {
        "username": "gleader21",
        "email": "gleader21@gmail.com",
        "password": "642@A531"
    }
    crud.create_user(db, **data)

    user = crud.authenticate_user(db,
                                  username="gleader21",
                                  password="642@A531")

    assert user is not None
