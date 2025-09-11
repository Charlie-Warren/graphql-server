import uvicorn
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from strawb.mutation import Mutation
from strawb.query import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)