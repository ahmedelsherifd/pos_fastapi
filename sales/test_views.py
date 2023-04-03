from fastapi.testclient import TestClient

from app.main import app
from .somedata import load_data


def test_create_order(db, client: TestClient):
    load_data(db)
    product = client.get("/variants/").json()[0]
    response = client.post("/orders/",
                           json={
                               "items": [{
                                   "product": product['id']
                               }],
                               "payment": {
                                   "amount": 100
                               }
                           })
    assert response.status_code == 200


def test_create_customer(db, client: TestClient):
    response = client.post("/customers/", json={"name": "Ahmed ELsherif"})
    assert response.status_code == 200


def test_create_product(db, client: TestClient):
    response = client.post("/products/",
                           json={
                               "name":
                               "Iphone 6",
                               "variants": [{
                                   "price": 10,
                                   "name": "Iphone 6 128GB",
                               }]
                           })
    assert response.status_code == 200


def test_create_category(db, client: TestClient):
    response = client.post("/categories/", json={"name": "Phones"})
    assert response.status_code == 200


def test_get_product_variants(db, client: TestClient):
    load_data(db)
    response = client.get("/variants/")
    assert response.status_code == 200


def test_get_categories(db, client: TestClient):
    load_data(db)
    response = client.get("/categories/")
    assert response.status_code == 200


def test_get_customers(db, client: TestClient):
    load_data(db)
    response = client.get("/customers/")
    assert response.status_code == 200


def test_get_sales_by_items(db, client: TestClient):
    load_data(db)
    response = client.get("/sales-by-items/")
    assert response.status_code == 200


def test_total_payments_daily(db, client: TestClient):
    load_data(db)
    response = client.get("/total-payments/")
    assert response.status_code == 200


def test_get_product(db, client: TestClient):
    load_data(db)
    response = client.get("/products/1/")
    assert response.status_code == 200


def test_get_customer(db, client: TestClient):
    load_data(db)
    response = client.get("/customers/1/")
    assert response.status_code == 200


def test_get_order(db, client: TestClient):
    load_data(db)
    response = client.get("/orders/1/")
    assert response.status_code == 200


def test_total_payments_node(db, client: TestClient):
    load_data(db)
    response = client.get("/total-payments/node/")
    assert response.status_code == 200