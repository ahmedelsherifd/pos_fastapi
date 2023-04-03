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
