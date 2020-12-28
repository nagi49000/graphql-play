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


def test_chinook_graphene_all_genres():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allGenres(first: 1) {edges {node {Name}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allGenres': {'edges': [{'node': {'Name': 'Rock'}}]}}}


def test_chinook_graphene_all_customers():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allCustomers(first: 1) {edges {node {FirstName}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allCustomers': {'edges': [{'node': {'FirstName': 'Luís'}}]}}}


def test_chinook_graphene_all_artists():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allArtists(first: 1) {edges {node {Name}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allArtists': {'edges': [{'node': {'Name': 'AC/DC'}}]}}}


def test_chinook_graphene_all_media_types():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allMediaTypes(first: 1) {edges {node {Name}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allMediaTypes': {'edges': [{'node': {'Name': 'MPEG audio file'}}]}}}


def test_chinook_graphene_all_playlists():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allPlaylists(first: 1) {edges {node {Name}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allPlaylists': {'edges': [{'node': {'Name': 'Music'}}]}}}


def test_chinook_graphene_all_albums():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allAlbums(first: 1) {edges {node {Title}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allAlbums': {
        'edges': [{'node': {'Title': 'For Those About To Rock We Salute You'}}]}}}


def test_chinook_graphene_all_invoices():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allInvoices(first: 1) {edges {node {InvoiceDate}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allInvoices': {
        'edges': [{'node': {'InvoiceDate': '2009-01-01T00:00:00'}}]}}}


def test_chinook_graphene_all_tracks():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allTracks(first: 1) {edges {node {Name}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allTracks': {
        'edges': [{'node': {'Name': 'For Those About To Rock (We Salute You)'}}]}}}


def test_chinook_graphene_all_invoice_items():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allInvoiceItems(first: 1) {edges {node {UnitPrice}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allInvoiceItems': {'edges': [{'node': {'UnitPrice': 0.99}}]}}}


def test_chinook_graphene_all_playlist_tracks():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{allPlaylistTracks(first: 1) {edges {node {TrackId}}}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {'data': {'allPlaylistTracks': {'edges': [{'node': {'TrackId': '1'}}]}}}


def test_chinook_graphene_customer():
    c = TestClient(get_app())
    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{customer(city:"Paris") {FirstName, City}}'})
    assert r.status_code == 200
    assert json.loads(r.text) == {
        "data": {
            "customer": [
                {
                    "FirstName": "Camille",
                    "City": "Paris"
                },
                {
                    "FirstName": "Dominique",
                    "City": "Paris"
                }
            ]
        }
    }

    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{customer{FirstName, City, State, Country}}'})
    assert r.status_code == 200
    assert len(json.loads(r.text)['data']['customer']) == 59

    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{customer(country: "USA"){FirstName, City, State, Country}}'})
    assert r.status_code == 200
    assert len(json.loads(r.text)['data']['customer']) == 13

    r = c.post('/chinook-graphene/api/v1/',
               json={'query': '{customer(country: "USA", state: "CA"){FirstName, City, State, Country}}'})
    assert r.status_code == 200
    assert len(json.loads(r.text)['data']['customer']) == 3
