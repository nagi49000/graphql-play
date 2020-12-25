from graphene import ObjectType, String, Schema
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'


def get_app():
    schema = Schema(query=Query)
    app = FastAPI()
    app.add_route("/faker/api/v1/", GraphQLApp(schema=schema))
    return app


app = get_app()
