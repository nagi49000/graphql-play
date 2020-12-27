import json
from starlette.testclient import TestClient
from ..graphene_app.simple_graphene_app import get_app


def test_simple_graphene_goodbye():
    c = TestClient(get_app())
    r = c.get('/simple-graphene/api/v1?query={goodbye}')
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'goodbye': 'See ya!'}}
    r = c.post('/simple-graphene/api/v1/',
               json={'query': '{goodbye}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'goodbye': 'See ya!'}}


def test_simple_graphene_hello():
    c = TestClient(get_app())
    r = c.post('/simple-graphene/api/v1/',
               json={'query': '{hello(name:"alice")}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'hello': 'Hello alice!'}}
    r = c.post('/simple-graphene/api/v1/',
               json={'query': '{hello(name:"bob")}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'hello': 'Hello bob!'}}


def test_simple_graphene_people():
    c = TestClient(get_app())
    r = c.post('/simple-graphene/api/v1/',
               json={'query': '{people {fullName, age}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {
        'data': {
            'people': [
                {
                    'age': 21,
                    'fullName': 'John Doe'
                }, {
                    'age': 24,
                    'fullName': 'Bob Boberson'
                }
            ]
        }
    }
    r = c.post('/simple-graphene/api/v1/',
               json={'query': '{people(maxAge:22) {firstName, lastName}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {
        'data': {
            'people': [
                {
                    'firstName': 'John',
                    'lastName': 'Doe'
                }
            ]
        }
    }


def test_chinook_graphene_version():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{version}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'version': '0.0.1'}}
