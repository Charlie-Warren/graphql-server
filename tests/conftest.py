import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.main import app
from app.database import Base, TEST_DATABASE_URL


@pytest.fixture(scope="function", autouse=True)
def clear_test_db():
    """
    Before each test, clear the test database.
    """
    #print("\n----------------\nClearing Test DB")
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_task(client: TestClient) -> dict:
    """
    Fixture that creates a task and returns it.
    """
    query = """
    mutation AddTask($title: String!) {
        addTask(title: $title) {
            id
            title
            completed
        }
    }
    """
    variables = {"title": "Fixture Task"}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    return response.json()["data"]["addTask"]


@pytest.fixture
def created_tasks(client: TestClient) -> list[dict]:
    """
    Fixture that creates 11 tasks and returns them.
    """
    tasks = []
    for i in range(11):
        query = """
        mutation AddTask($title: String!) {
            addTask(title: $title) {
                id
                title
                completed
            }
        }
        """
        variables = {"title": f"Fixture Task {i}"}
        response = client.post("/graphql", json={"query": query, "variables": variables})
        tasks.append(response.json()["data"]["addTask"])
    return tasks