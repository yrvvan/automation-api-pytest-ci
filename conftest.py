import pytest

@pytest.fixture
def sample_payload():
    return {"title": "foo", "body": "bar", "userId": 1}
