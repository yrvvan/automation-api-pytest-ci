import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_post(sample_payload):
    response = requests.post(f"{BASE_URL}/posts", json=sample_payload)
    assert response.status_code == 204
    assert response.json()["title"] == sample_payload["title"]
