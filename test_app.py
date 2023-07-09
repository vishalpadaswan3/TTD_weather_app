import json
import pytest
from app import app, weather_data



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_weather():
    response = app.test_client().get('/weather/San%20Francisco')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['temperature'] == 14
    assert data['weather'] == 'Cloudy'

def test_add_weather(client):
    response = client.post(
        '/weather',
        json={'city': 'Chicago', 'temperature': 18, 'weather': 'Cloudy'}
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'message' in data
    assert 'Weather information added' in data['message']
    assert 'Chicago' in weather_data

def test_update_weather(client):
    response = client.put(
        '/weather/Chicago',
        json={'temperature': 20}
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'message' in data
    assert 'Weather information updated' in data['message']
    assert weather_data['Chicago']['temperature'] == 20

def test_delete_weather(client):
    response = client.delete('/weather/Chicago')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'message' in data
    assert 'Weather information deleted' in data['message']
    assert 'Chicago' not in weather_data


def test_get_weather_not_found(client):
    response = client.get('/weather/UnknownCity')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert 'error' in data
    assert 'Weather information not found' in data['error']

def test_add_weather_missing_fields(client):
    response = client.post(
        '/weather',
        json={'city': 'Boston', 'temperature': 25}
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert 'error' in data
    assert 'Missing required fields' in data['error']

def test_update_weather_not_found(client):
    response = client.put(
        '/weather/UnknownCity',
        json={'temperature': 22}
    )
    data = json.loads(response.data)

    assert response.status_code == 404
    assert 'error' in data
    assert 'Weather information not found' in data['error']

def test_delete_weather_not_found(client):
    response = client.delete('/weather/UnknownCity')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert 'error' in data
    assert 'Weather information not found' in data['error']


