from fastapi.testclient import TestClient

added_ids = []

def test_add_task(client: TestClient):
    query = """
    mutation AddTask($title: String!) {
        addTask(title: $title) {
            id
            title
            completed
        }
    }
    """
    variables = {"title": "Test Task"}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["addTask"]
    added_ids.append(data["id"])

    assert response.status_code == 200
    assert data["title"] == "Test Task"
    assert data["completed"] is False


def test_task(client: TestClient):
    query = """
    query Task($id: ID!) {
        task(id: $id) {
            id
            title
            completed
        }
    }
    """
    id = added_ids[0]
    variables = {"id": id}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["task"]

    assert response.status_code == 200
    assert data["id"] == id


def test_tasks(client: TestClient):
    query = """
    query {
        tasks {
            id
            title
            completed
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    data = response.json()["data"]["tasks"]
    assert response.status_code == 200
    assert len(data) > 0


def test_toggle_task(client: TestClient):
    # Get the ID of the first task, added earlier
    id = added_ids[0]
    
    # Try to toggle it to True
    query = """
    mutation ToggleTask($id: ID!) {
        toggleTask(id: $id) {
            id
            title
            completed
        }
    }
    """
    variables = {"id": id}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["toggleTask"]

    assert response.status_code == 200
    assert data["completed"]


def test_delete_task(client: TestClient):
    # Get the ID of the first task, added earlier
    id = added_ids[0]
    
    query = """
    mutation DeleteTask($id: ID!) {
        deleteTask(id: $id) {
            id
            title
            completed
        }
    }
    """
    variables = {"id": id}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["deleteTask"]

    assert response.status_code == 200

    # Check that the task was deleted
    query = """
    query Task($id: ID!) {
        task(id: $id) {
            id
            title
            completed
        }
    }
    """
    variables = {"id": id}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["task"]

    assert response.status_code == 200
    assert data is None
