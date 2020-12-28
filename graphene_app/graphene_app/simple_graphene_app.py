import datetime
import os
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import graphene as gp
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp

# simple no database example


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


# Database example
# Database specific stuff

def get_declarative_base_class_and_engine(sql_db=None):
    if sql_db is None:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        sql_db = 'sqlite:///' + os.path.join(this_dir, '..', '..', 'data', 'chinook.db')
    sql_engine = sa.engine.create_engine(sql_db)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=sql_engine))
    Base = declarative_base(cls=DeferredReflection)
    Base.query = db_session.query_property()
    return sql_engine, Base


sql_engine, Base = get_declarative_base_class_and_engine()

# Build up the Data models, using sqlalchemy.ext.declarative to
# pull in the models from the SQL DB Metadata


class CustomerModel(Base):
    __tablename__ = 'customers'
    # CustomerId = sa.Column(sa.Integer, primary_key=True)


class ArtistModel(Base):
    __tablename__ = 'artists'


class EmployeeModel(Base):
    __tablename__ = 'employees'


class GenreModel(Base):
    __tablename__ = 'genres'


class MediaTypeModel(Base):
    __tablename__ = 'media_types'


class PlaylistModel(Base):
    __tablename__ = 'playlists'


class AlbumModel(Base):
    __tablename__ = 'albums'


class InvoiceModel(Base):
    __tablename__ = 'invoices'


class TrackModel(Base):
    __tablename__ = 'tracks'


class InvoiceItemModel(Base):
    __tablename__ = 'invoice_items'


class PlaylistTrackModel(Base):
    __tablename__ = 'playlist_track'


Base.prepare(sql_engine)

# GraphQL schema specific stuff
# Build up the Graphene objects that will make up the Graph QL schema


class Customer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerModel
        interfaces = (gp.relay.Node, )


class Artist(SQLAlchemyObjectType):
    class Meta:
        model = ArtistModel
        interfaces = (gp.relay.Node, )


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (gp.relay.Node, )


class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel
        interfaces = (gp.relay.Node, )


class MediaType(SQLAlchemyObjectType):
    class Meta:
        model = MediaTypeModel
        interfaces = (gp.relay.Node, )


class Playlist(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistModel
        interfaces = (gp.relay.Node, )


class Album(SQLAlchemyObjectType):
    class Meta:
        model = AlbumModel
        interfaces = (gp.relay.Node, )


class Invoice(SQLAlchemyObjectType):
    class Meta:
        model = InvoiceModel
        interfaces = (gp.relay.Node, )


class Track(SQLAlchemyObjectType):
    class Meta:
        model = TrackModel
        interfaces = (gp.relay.Node, )


class InvoiceItem(SQLAlchemyObjectType):
    class Meta:
        model = InvoiceItemModel
        interfaces = (gp.relay.Node, )


class PlaylistTrack(SQLAlchemyObjectType):
    class Meta:
        model = PlaylistTrackModel
        interfaces = (gp.relay.Node, )


class Chinook(gp.ObjectType):
    version = gp.String()
    # use SQLAlchemyConnectionField to build up queries for
    # Graphene objects above. Standard queries pull ALL rows
    node = gp.relay.Node.Field()  # not sure why this is needed...
    all_customers = SQLAlchemyConnectionField(Customer.connection)
    all_employees = SQLAlchemyConnectionField(Employee.connection)
    all_artists = SQLAlchemyConnectionField(Artist.connection)
    all_genres = SQLAlchemyConnectionField(Genre.connection)
    all_media_types = SQLAlchemyConnectionField(MediaType.connection)
    all_playlists = SQLAlchemyConnectionField(Playlist.connection)
    all_albums = SQLAlchemyConnectionField(Album.connection)
    all_invoices = SQLAlchemyConnectionField(Invoice.connection)
    all_tracks = SQLAlchemyConnectionField(Track.connection)
    all_invoice_items = SQLAlchemyConnectionField(InvoiceItem.connection)
    all_playlist_tracks = SQLAlchemyConnectionField(PlaylistTrack.connection)
    customer = gp.NonNull(gp.List(gp.NonNull(Customer)),
                          city=gp.String(default_value=''),
                          state=gp.String(default_value=''),
                          country=gp.String(default_value=''))
    employee = gp.NonNull(gp.List(gp.NonNull(Employee)),
                          min_birth_date=gp.DateTime(default_value="1900-01-01T00:00:00"),
                          max_birth_date=gp.DateTime(default_value="2100-01-01T00:00:00"))

    async def resolve_version(root, info):
        return "0.0.1"

    async def resolve_customer(root, info, city, state, country):
        query = Customer.get_query(info=info)
        if city:
            query = query.filter(CustomerModel.City == city)
        if state:
            query = query.filter(CustomerModel.State == state)
        if country:
            query = query.filter(CustomerModel.Country == country)
        return query.all()

    async def resolve_employee(root, info, min_birth_date, max_birth_date):
        query = Employee.get_query(info=info)
        query = query.filter(EmployeeModel.BirthDate >= min_birth_date)
        query = query.filter(EmployeeModel.BirthDate <= max_birth_date)
        return query.all()


def get_app():
    routes = [
        Route("/simple-graphene/api/v1/",
              GraphQLApp(schema=gp.Schema(query=ToySimples))),
        Route("/chinook-graphene/api/v1/",
              GraphQLApp(schema=gp.Schema(query=Chinook, types=[Customer]),
                         executor_class=AsyncioExecutor))
    ]
    return Starlette(routes=routes)


# can run in this directory at the cmd line with
# uvicorn simple_graphene_app:app
app = get_app()
