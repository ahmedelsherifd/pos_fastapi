from os import environ
import pytest

environ["TESTING"] = str(True)


@pytest.fixture
def db():
    from app.database import SessionLocal
    db = SessionLocal()
    return db


@pytest.fixture(autouse=True)
def database_setup_teardown(db, request):
    from app.database import Base, engine
    Base.metadata.create_all(engine)

    def drop_tables():
        Base.metadata.drop_all(engine)

    request.addfinalizer(drop_tables)
