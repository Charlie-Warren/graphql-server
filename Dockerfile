FROM python:3.10-slim

WORKDIR /graphql-server

COPY pyproject.toml .

RUN pip install .

COPY app ./app

CMD ["python", "-m", "app.main"]
