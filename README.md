# graphql-server
An example GraphQL server using FastAPI and Strawberry GraphQL.

## Installation
Install by running:
```
pip install .
```

Alternatively, if you are using [uv package manager](https://docs.astral.sh/uv/), you can simply run:
```
uv sync
```
This will setup a venv and install the requirements in one step.

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