import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from alembic import command
from alembic.config import Config

from app.main import app
from app.dependencies.db import get_db


@pytest.fixture(scope="session")
def test_database_url() -> str:
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        raise RuntimeError("TEST_DATABASE_URL is not set. Set it in your environment/.env for tests.")
    return url


@pytest.fixture(scope="session")
def engine(test_database_url: str):
    engine = create_engine(test_database_url)
    return engine


@pytest.fixture(scope="session", autouse=True)
def apply_migrations(test_database_url: str):
    # AlembicをテストDBへ適用
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_database_url)
    command.upgrade(alembic_cfg, "head")
    yield


@pytest.fixture()
def db_session(engine) -> Session:
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session: Session):
    # 依存注入をテスト用に差し替え
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
