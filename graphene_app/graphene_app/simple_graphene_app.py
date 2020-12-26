import os
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker
import graphene as gp
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp


# Database specific stuff


this_dir = os.path.dirname(os.path.abspath(__file__))
sql_db = 'sqlite:///' + os.path.join(this_dir, '..', '..', 'data', 'chinook.db')
sql_engine = sa.engine.create_engine(sql_db)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=sql_engine))
Base = declarative_base(cls=DeferredReflection)
Base.query = db_session.query_property()


class CustomerModel(Base):
    __tablename__ = 'customers'
    CustomerId = sa.Column(sa.Integer, primary_key=True)


Base.prepare(sql_engine)

# GraphQL schema specific stuff


class Customer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerModel
        interfaces = (gp.relay.Node, )


class Person(gp.ObjectType):
    firstName = gp.String(required=True)
    lastName = gp.String(required=True)
    age = gp.Int(required=True)
    fullName = gp.String()


class ToySimples(gp.ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = gp.String(name=gp.String(default_value="stranger"))
    goodbye = gp.String()
    people = gp.NonNull(gp.List(gp.NonNull(Person)),
                        max_age=gp.Int(default_value=60))

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


class Chinook(gp.ObjectType):
    version = gp.String()
    node = gp.relay.Node.Field()
    customer = gp.List(Customer)

    def resolve_version(root, info):
        return "0.0.1"

    def resolve_customer(self, info):
        print(info)
        query = Customer.get_query(info)
        print(query)
        return query.all()


def get_app():
    routes = [Route("/simple-graphene/api/v1/",
                    GraphQLApp(schema=gp.Schema(query=ToySimples))),
              Route("/chinook-graphene/api/v1/",
                    GraphQLApp(schema=gp.Schema(query=Chinook, types=[Customer]),
                               executor_class=AsyncioExecutor))]
    return Starlette(routes=routes)


# can run in this directory at the cmd line with
# uvicorn simple_graphene_app:app
app = get_app()
