from fastapi.testclient import TestClient


def test_add_task(client: TestClient):
    """
    Test that a task is added correctly to an empty database. completed should be false for the new task
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
    variables = {"title": "Test Task"}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["addTask"]

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] == False


def test_toggle_task(client: TestClient, created_task):
    """
    Test that after making a new task and toggling it, its new value is True
    """
    query = """
    mutation ToggleTask($id: ID!) {
        toggleTask(id: $id) {
            id
            completed
        }
    }
    """
    variables = {"id": created_task["id"]}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["toggleTask"]

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert data["completed"] == True


def test_toggle_task_not_found(client: TestClient):
    """
    Test that a task is not found in an empty database
    """
    query = """
    mutation ToggleTask($id: ID!) {
        toggleTask(id: $id) {
            id
            completed
        }
    }
    """
    variables = {"id": "123"}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]
    error_count = len(response.json()["errors"])
    error_messages = [response.json()["errors"][i]["message"] for i in range(error_count)]

    assert response.status_code == 200
    assert "errors" in response.json()
    # check "not found" appears at least partially in at least one of the error messages
    assert any("not found" in error_message for error_message in error_messages)
    assert data is None


def test_delete_task(client: TestClient, created_task):
    """
    Test deleting a task, and then confirming it has been deleted
    """
    query = """
    mutation DeleteTask($id: ID!) {
        deleteTask(id: $id) {
            id
        }
    }
    """
    variables = {"id": created_task["id"]} # Get the id of the task added by created_task
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["deleteTask"]

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert data["id"] == created_task["id"]

    # Confirm deletion
    query = """
    query Task($id: ID!) {
        task(id: $id) {
            id
        }
    }
    """
    variables = {"id": created_task["id"]}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["task"]

    error_count = len(response.json()["errors"])
    error_messages = [response.json()["errors"][i]["message"] for i in range(error_count)]

    assert response.status_code == 200
    assert "errors" in response.json()
    # check "not found" appears at least partially in at least one of the error messages
    assert any("not found" in error_message for error_message in error_messages)
    assert data is None
