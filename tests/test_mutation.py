from fastapi.testclient import TestClient


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
    print(response.json())
    data = response.json()["data"]["addTask"]

    assert response.status_code == 200
    assert data["title"] == "Test Task"
    assert data["completed"] is False


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
    #id = data[0]["id"]
    assert response.status_code == 200
    assert len(data) > 0


def test_toggle_task(client: TestClient):
    # Get the ID of the first task
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
    id = data[0]["id"]
    
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