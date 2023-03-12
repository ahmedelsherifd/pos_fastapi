from .crud import create_customer, create_product, create_order, get_customers, get_products
from app.database import Base
from . import models

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_pos_create_order():
    # setup
    Base.metadata.create_all(engine)
    db = SessionLocal()

    customer_input = {"name": "Ahmed ELsherif"}

    customer = create_customer(db, **customer_input)

    Base.metadata.drop_all(engine)

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

    create_product(**product_1_input)
    create_product(**product_2_input)
    # test crud functions that should work in POS
    customer = get_customers().first()
    products = get_products()

    product_1 = products[0]
    product_2 = products[1]

    order_input = {
        "customer": customer,
        "items": [{
            "product": product_1
        }, {
            "product": product_2
        }]
    }

    order = create_order(**order_input)

    assert order.id is not None
    assert order.total_price == 20
