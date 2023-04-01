from os import environ
import pytest

environ["TESTING"] = str(True)


@pytest.fixture
def db(request):
    from app.database import engine, SessionLocal

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
