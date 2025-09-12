import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.main import app
from app.database import Base, TEST_DATABASE_URL


@pytest.fixture(scope="session", autouse=True)
def teardown():
    yield
    # when all the tests have run,
    # connect to the Test DB and drop all tables
    print("\n----------------\nClearing Test DB")
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()


@pytest.fixture
def client():
    return TestClient(app)
