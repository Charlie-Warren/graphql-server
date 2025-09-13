FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y

WORKDIR /graphql-server

COPY pyproject.toml .

RUN pip install .

COPY app ./app

CMD ["python", "-m", "app.main"]
