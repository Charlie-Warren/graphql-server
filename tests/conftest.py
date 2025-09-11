import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use monkey patch to allow using TestingSessionLocal instead
@pytest.fixture(scope="function", autouse=True)
def setup_db(monkeypatch):
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr("database.SessionLocal", TestingSessionLocal)
    yield
    # Drop tables after test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
