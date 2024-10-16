import os
import pytest
import requests

# You might want to load these from a config file
BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
API_KEY = os.getenv('API_KEY', 'your-api-key')

@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    })
    return session

def test_get_user(api_client):
    response = api_client.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    user_data = response.json()
    assert "id" in user_data
    assert "name" in user_data

def test_create_user(api_client):
    new_user = {"name": "John Doe", "email": "john@example.com"}
    response = api_client.post(f"{BASE_URL}/users", json=new_user)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["name"] == new_user["name"]
    assert created_user["email"] == new_user["email"]

    # Clean up: delete the created user
    user_id = created_user["id"]
    delete_response = api_client.delete(f"{BASE_URL}/users/{user_id}")
    assert delete_response.status_code == 204

@pytest.mark.parametrize("user_id, expected_status", [
    (1, 200),  # Assuming user 1 always exists
    (99999, 404),  # Assuming this user doesn't exist
])
def test_get_user_error_handling(api_client, user_id, expected_status):
    response = api_client.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == expected_status

# Example of using pytest-mock with actual API calls
def test_api_timeout(api_client, mocker):
    # Mock the api_client's get method to simulate a timeout
    mocker.patch.object(api_client, 'get', side_effect=requests.Timeout)

    with pytest.raises(requests.Timeout):
        api_client.get(f"{BASE_URL}/users/1")