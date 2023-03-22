from os import environ
import pytest

environ["TESTING"] = str(True)


@pytest.fixture()
def db():
    from app.database import Base, engine, SessionLocal

    Base.metadata.create_all(engine)
    db = SessionLocal()
    yield db
    Base.metadata.drop_all(engine)
