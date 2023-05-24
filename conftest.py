from os import environ

import pytest
from fastapi.testclient import TestClient
from starlette_context import context
from sqlalchemy.orm import Session

environ["TESTING"] = str(True)


def admin_headers(db: Session, client: TestClient):
    from sales.crud import create_user

    data = {
        "username": "admin",
        "password": "A*457951",
    }
    create_user(db, **data, email="admin@gmail.com")
    response = client.post("/token/", data=data)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


@pytest.fixture
def db(request):
    from app.database import SessionLocal, engine

    connection = engine.connect()
    transaction = connection.begin()

    db = SessionLocal(bind=connection)

    def roll_back():
        db.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(roll_back)
    return db


@pytest.fixture(scope="session", autouse=True)
def database_setup(request):
    from app.database import Base, engine
    Base.metadata.create_all(engine)

    def drop_tables():
        Base.metadata.drop_all(engine)

    request.addfinalizer(drop_tables)


@pytest.fixture()
def client(db):
    from app.main import app, get_db

    def overid_get_db():
        try:
            context.data["db"] = db
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = overid_get_db
    # headers = admin_headers(db, TestClient(app))
    with TestClient(app) as c:
        c.headers = admin_headers(db, c)
        yield c