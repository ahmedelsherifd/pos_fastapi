from os import environ

import pytest
from fastapi.testclient import TestClient
from starlette_context import context

from app.main import app, get_db

environ["TESTING"] = str(True)


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

    def overid_get_db():
        try:
            context.data["db"] = db
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = overid_get_db

    with TestClient(app) as c:
        yield c