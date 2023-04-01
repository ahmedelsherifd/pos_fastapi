from os import environ
from sqlalchemy.orm import Session
import pytest

environ["TESTING"] = str(True)


@pytest.fixture
def db(request):
    from app.database import Base, engine
    Base.metadata.create_all(engine)

    connection = engine.connect()
    transaction = connection.begin()

    db = Session(bind=connection)

    def roll_back():
        db.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(roll_back)
    return db


# @pytest.fixture(autouse=True)
# def database_setup_teardown(db: Session, request):
#     from app.database import Base, engine
#     Base.metadata.create_all(engine)

#     def drop_tables():
#         # Base.metadata.drop_all(engine)
#         # roll back
#         db.rollback()
#         pass

#     request.addfinalizer(drop_tables)
