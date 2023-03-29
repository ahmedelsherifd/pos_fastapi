import pytest

from . import models
from .crud import (create_category, create_customer, create_order,
                   create_product, get_customers, get_order,
                   get_sales_by_items, get_variants)


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


def test_filter_product_by_catgory(db):
    cars_cat = create_category(db, name="Cars")
    phones_cat = create_category(db, name="Phones")

    product_1_input = {
        "name": "Honda CRV 2023",
        "category": cars_cat,
        "variants": [{
            "price": 100,
            "name": "Honda CRV 2023 Grey",
            "SKU": "4578"
        }]
    }
    product_2_input = {
        "name": "Iphone 12",
        "category": phones_cat,
        "variants": [{
            "price": 20,
            "name": "Iphone 12 128GB",
            "SKU": "4589"
        }]
    }
    create_product(db, **product_1_input)
    create_product(db, **product_2_input)

    products = get_variants(db, category=phones_cat.id)
    assert products[0].name == "Iphone 12 128GB"
    assert len(products) == 1


def test_sales_by_items(db):
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

    varinats = get_variants(db)

    variant_1 = varinats[0]
    variant_2 = varinats[1]

    order_input = {
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

    create_order(db, **order_input)

    order_input = {
        "items": [{
            "product": variant_1,
            "quantity": 10
        }],
        "payment": {
            "amount": 100
        }
    }

    create_order(db, **order_input)

    sales_by_item = get_sales_by_items(db)

    item_1 = sales_by_item[0]

    assert item_1.ProductVariant.name == "Iphone 12 128GB"
    assert item_1.total_sales == 110
    assert item_1.total_quantity == 11
