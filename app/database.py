from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from starlette_context import context

from .settings import Settings

settings = Settings()

if settings.TESTING:
    SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):

    @classmethod
    def from_id(cls, id: int):
        db = context["db"]
        stmt = select(cls).where(cls.id == id)
        result = db.scalar(stmt)
        return result
