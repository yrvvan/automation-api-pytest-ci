import os
import pytest
import requests
from dotenv import load_dotenv
from helpers.schema_validator import validate_json_schema

load_dotenv()  # Load environment variables from .env
BASE_URL = os.getenv("BASE_URL")

@pytest.mark.get #tagging GET
def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    validate_json_schema(response.json(), "get.json")

@pytest.mark.post #tagging POST
def test_create_post(sample_payload):
    response = requests.post(f"{BASE_URL}/posts", json=sample_payload)
    assert response.status_code == 201
    assert response.json()["title"] == sample_payload["title"]
