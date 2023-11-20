from fastapi import FastAPI
from graphene import Schema
from starlette.middleware.cors import CORSMiddleware
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.gql.mutations import Mutation
from app.gql.queries import Query
from app.utils.database import create_database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = Schema(query=Query, mutation=Mutation)


@app.on_event("startup")  # TODO: Remove that on production
def test() -> None:
    create_database()


app.mount("/", GraphQLApp(schema=schema, on_get=make_playground_handler()))
