from graphene import ObjectType, String, Int, List, NonNull, Schema
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp


class Person(ObjectType):
    firstName = String(required=True)
    lastName = String(required=True)
    age = Int(required=True)
    fullName = String()


class ToySimples(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()
    people = NonNull(List(NonNull(Person)),
                     max_age=Int(default_value=60))

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_people(root, info, max_age):
        data = [["John", "Doe", 21], ["Bob", "Boberson", 24]]
        return [Person(firstName=x, lastName=y, age=z, fullName=x+' '+y)
                for x, y, z in data
                if z <= max_age]


class Chinook(ObjectType):
    version = String()

    def resolve_version(root, info):
        return "0.0.1"


def get_app():
    schema = Schema(query=ToySimples)
    routes = [Route("/simple-graphene/api/v1/",
                    GraphQLApp(schema=schema,
                               executor_class=AsyncioExecutor))]
    return Starlette(routes=routes)


# can run in this directory at the cmd line with
# uvicorn simple_graphene_app:app
app = get_app()
