from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./pos_app.db"
    TEST_DATABASE_URL: str = "sqlite:///./test_pos_app.db"
    TESTING: bool = False
