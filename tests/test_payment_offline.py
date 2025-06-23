import os
import json
import pytest
import requests
from pathlib import Path
from dotenv import load_dotenv
from helpers.schema_validator import validate_json_schema

load_dotenv()

ENV = os.getenv("ENV")
API_PORTAL = os.getenv("API_PORTAL")

if ENV != "prod":
    API_PORTAL_HOST = f"https://{ENV}-{API_PORTAL}"
else:
    API_PORTAL_HOST = f"https://{API_PORTAL}"

# File paths
BASE_DIR = Path(__file__).resolve().parent
ADMIN_TOKEN_PATH = BASE_DIR / "../fixtures/admin_token.json"
DATA_PATH = BASE_DIR / "../fixtures/data/payment_offline_data.json"

# Load admin token
with open(ADMIN_TOKEN_PATH, "r", encoding="utf-8") as file:
    admin_tokens = json.load(file)
admin_token = admin_tokens.get(ENV)

# Load test data
with open(DATA_PATH, "r", encoding="utf-8") as file:
    payload_data = json.load(file)
valid_payload = payload_data["post"]["validData"]


@pytest.mark.post  # tagging POST
def test_payment_offline():
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=valid_payload
    )
    assert response.status_code == 200
    assert response.json().get("code") == "OK"
    validate_json_schema(response.json(), "post_payment_offline_schema.json")
