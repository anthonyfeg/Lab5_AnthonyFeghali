import sqlite3
import pytest
import database
from app import app

USER = dict(name='Jane Example', email='jane@example.com', phone='0123456789',
            address='Test Street', country='Lebanon')

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, 'DATABASE', tmp_path / 'test.db')
    database.create_db_table()
    app.config.update(TESTING=True)
    return app.test_client()


def test_crud_and_sqlite_persistence(client):
    assert client.get('/api/users').json == []
    response = client.post('/api/users/add', json=USER)
    assert response.status_code == 201
    user_id = response.json['user_id']
    assert client.get(f'/api/users/{user_id}').json == {**USER, 'user_id': user_id}
    assert len(client.get('/api/users').json) == 1
    updated = {**USER, 'name': "Jane O'Brien", 'user_id': user_id}
    assert client.put('/api/users/update', json=updated).json == updated
    # Verify persistence using an independent SQLite connection.
    with sqlite3.connect(database.DATABASE) as conn:
        assert conn.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0] == "Jane O'Brien"
    assert client.get(f'/api/users/{user_id}').json == updated
    assert client.delete(f'/api/users/delete/{user_id}').status_code == 200
    assert client.get(f'/api/users/{user_id}').status_code == 404
    assert client.get('/api/users').json == []


@pytest.mark.parametrize('payload', [None, [], {}, {**USER, 'email': ''}, {**USER, 'phone': 123}])
def test_invalid_payload(client, payload):
    response = client.post('/api/users/add', data=__import__('json').dumps(payload), content_type='application/json')
    assert response.status_code == 400
    assert client.get('/api/users').json == []


def test_missing_user_and_bad_id(client):
    assert client.get('/api/users/999').status_code == 404
    assert client.delete('/api/users/delete/999').status_code == 404
    assert client.put('/api/users/update', json={**USER, 'user_id': 999}).status_code == 404
    assert client.put('/api/users/update', json={**USER, 'user_id': True}).status_code == 400
    assert client.get('/api/users/not-a-number').status_code == 404


def test_bad_json_content_type_and_cors(client):
    assert client.post('/api/users/add', data='{', content_type='application/json').status_code == 400
    assert client.post('/api/users/add', data='text').status_code == 415
    response = client.options('/api/users/add', headers={'Origin':'http://localhost:3000','Access-Control-Request-Method':'POST'})
    assert response.status_code == 200
    assert response.headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'


def test_idempotent_schema(client):
    client.post('/api/users/add', json=USER)
    database.create_db_table()
    assert len(client.get('/api/users').json) == 1
