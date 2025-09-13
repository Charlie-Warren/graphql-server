import requests

GRAPHQL_URL = "http://127.0.0.1:8000/graphql"

query_all_tasks = """
query {
    tasks {
        id
        title
        completed
        createdAt
        updatedAt
    }
}
"""

query_single_task = """
query($id: ID!) {
    task(id: $id) {
        id
        title
        completed
        createdAt
        updatedAt
    }
}
"""

mutation_add_task = """
mutation($title: String!) {
    addTask(title: $title) {
        id
        title
        completed
        createdAt
        updatedAt
    }
}
"""

mutation_toggle_task = """
mutation($id: ID!) {
    toggleTask(id: $id) {
        id
        title
        completed
    }
}
"""

mutation_delete_task = """
mutation($id: ID!) {
    deleteTask(id: $id) {
        id
        title
    }
}
"""


def run_query(query, variables=None):
    response = requests.post(GRAPHQL_URL, json={"query": query, "variables": variables})
    return response.json()


if __name__ == "__main__":
    new_task = run_query(mutation_add_task, {"title": "Test task"})
    print("Add task:", new_task)

    task_id = new_task["data"]["addTask"]["id"]

    all_tasks = run_query(query_all_tasks)
    print("All tasks:", all_tasks)

    toggled = run_query(mutation_toggle_task, {"id": task_id})
    print("Toggled task:", toggled)

    single_task = run_query(query_single_task, {"id": task_id})
    print("Single task:", single_task)

    deleted = run_query(mutation_delete_task, {"id": task_id})
    print("Deleted task:", deleted)