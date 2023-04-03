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
