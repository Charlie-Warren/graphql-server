
def test_add_task(client):
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
    assert data["title"] == "Test Task"
    assert data["completed"] is False
