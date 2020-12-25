from graphene import ObjectType, String, Int, List, NonNull, Schema
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


class Person(ObjectType):
    firstName = String()
    lastName = String()
    age = Int()
    fullName = String()


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()
    people = NonNull(List(NonNull(Person)))

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_people(root, info):
        return [Person(firstName=x, lastName=y, age=z, fullName=x+' '+y)
                for x, y, z in [["John", "Doe", 21], ["Bob", "Boberson", 24]]]


def get_app():
    schema = Schema(query=Query)
    app = FastAPI()
    app.add_route("/faker/api/v1/", GraphQLApp(schema=schema))
    return app


app = get_app()
