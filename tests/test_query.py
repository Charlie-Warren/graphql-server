from fastapi.testclient import TestClient


def test_task(client: TestClient, created_task):
    """
    Test that a task is found correctly in a database with one task
    """
    query = """
    query Task($id: ID!) {
        task(id: $id) {
            id
            title
            completed
        }
    }
    """
    pre_added_id = created_task["id"]
    variables = {"id": pre_added_id}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["task"]

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert data["id"] == pre_added_id # Check the id is the same as the one we added in created_task


def test_task_not_found(client: TestClient):
    """
    Test that a task is not found in an empty database
    """
    query = """
    query Task($id: ID!) {
        task(id: $id) {
            id
            title
            completed
        }
    }
    """
    variables = {"id": "123"}
    response = client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()["data"]["task"]
    error_count = len(response.json()["errors"])
    error_messages = [response.json()["errors"][i]["message"] for i in range(error_count)]

    assert response.status_code == 200
    assert "errors" in response.json()
    # check "not found" appears at least partially in at least one of the error messages
    assert any("not found" in error_message for error_message in error_messages)
    assert data is None
    

def test_tasks(client: TestClient, created_tasks):
    """
    Test that all tasks are found correctly
    """
    query = """
    query {
        tasks {
            id
            title
            completed
        }
    }
    """
    number_of_added_tasks = len(created_tasks)
    response = client.post("/graphql", json={"query": query})
    data = response.json()["data"]["tasks"]

    assert response.status_code == 200
    assert "errors" not in response.json()
    assert len(data) == number_of_added_tasks


def test_tasks_filter(client: TestClient, created_tasks):
    """
    Test that tasks are filtered correctly. Should only return two tasks with 0 in the title
    """
    query = """
    query {
        tasks(search: "0") {
            id
            title
            completed
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    data = response.json()["data"]["tasks"]

    assert response.status_code == 200
    assert "errors" not in response.json()
    # There should be exactly two tasks with 0 in: "Fixture Task 0" and "Fixture Task 10"
    assert len(data) == 2