# graphql-server
An example GraphQL server using FastAPI and Strawberry GraphQL.

## Installation
Install by running:
```
pip install .
```
Adding the `[dev]` flag is required for running the pytest tests.

Alternatively, if you are using [uv package manager](https://docs.astral.sh/uv/), you can simply run:
```
uv sync
```
This will setup a venv and install the requirements in one step.
Adding the `--dev` flag is required for running the pytest tests.

## Testing

To run the tests, first ensure you installed the optional `dev` dependencies. Then run:
```
pytest
```

## Running the Server

### A) Running locally
To start the server, run:
```
python -m app.main
```

### B) Running a Container
A Dockerfile has been provided if you prefer to run the server in a container.

To build the image, run:
```
docker build -t graphql-server .
```

To run the container, run:
```
docker run --rm -it -p 8000:8000 graphql-server
```

## Future Considerations

In future, I would like to add the following:
- More thorough tests
- Authentication and Users, so individuals can only acces their own task list
- A `tasks_by_status()` query, that filters tasks by whether they are incomplete or complete
- An `update_task()` mutation, that allows updating the title of a task (and incidentally updating the `updated_at` timestamp)