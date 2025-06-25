import os
import json
import copy
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


def deep_copy(obj):
    return copy.deepcopy(obj)


@pytest.mark.post  # tagging POST
def test_payment_offline_valid():
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=valid_payload
    )
    assert response.status_code == 200
    assert response.json().get("code") == "OK"
    validate_json_schema(response.json(), "post_payment_offline_schema.json")


@pytest.mark.post  # tagging POST
def test_payment_offline_duplicate_name():
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=valid_payload
    )
    assert response.status_code == 400
    assert response.json().get("code") == "PAYMENT_NAME_DUPLICATE"


@pytest.mark.post  # tagging POST
def test_payment_offline_empty_auth():
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer ",
                 "Content-Type": "application/json"},
        json=valid_payload
    )
    assert response.status_code == 401
    assert response.json().get("error") == "Unauthorized"


@pytest.mark.post  # tagging POST
def test_payment_offline_empty_payment_name():
    modified_payload = deep_copy(valid_payload)
    modified_payload["name"] = ""
    
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=modified_payload
    )
    assert response.status_code == 400
    assert response.json().get("error") == "name must not be blank"


@pytest.mark.post  # tagging POST
def test_payment_offline_empty_service_type():
    modified_payload = deep_copy(valid_payload)
    modified_payload["serviceType"] = []
    
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=modified_payload
    )
    assert response.status_code == 400


@pytest.mark.post  # tagging POST
def test_payment_offline_invalid_service_type():
    modified_payload = deep_copy(valid_payload)
    modified_payload["serviceType"] = ["MAKAN_DI_TEMPAT"]
    
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=modified_payload
    )
    assert response.status_code == 400


@pytest.mark.post  # tagging POST
def test_payment_offline_empty_payment_type():
    modified_payload = deep_copy(valid_payload)
    modified_payload["type"] = ""
    
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=modified_payload
    )
    assert response.status_code == 400


@pytest.mark.post  # tagging POST
def test_payment_offline_invalid_payment_type():
    modified_payload = deep_copy(valid_payload)
    modified_payload["type"] = "vwxyz"
    
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=modified_payload
    )
    assert response.status_code == 400


@pytest.mark.post  # tagging POST
def test_payment_offline_is_record_send_string():
    modified_payload = deep_copy(valid_payload)
    modified_payload["isRecordAndDisplay"] = "TRUE"
    
    response = requests.post(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=modified_payload
    )
    assert response.status_code == 400


@pytest.mark.post  # tagging POST
def test_payment_offline_method_not_allowed():
    response = requests.delete(
        f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=2213",
        headers={"Authorization": f"Bearer {admin_token}",
                 "Content-Type": "application/json"},
        json=valid_payload
    )
    assert response.status_code == 405
    assert response.json().get("error") == "Method Not Allowed"


# @pytest.mark.post  # tagging POST
# def test_delete_payment_offline_store_not_found():
#     response = requests.delete(
#         f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=12390",
#         headers={"Authorization": f"Bearer {admin_token}",
#                  "Content-Type": "application/json"},
#         json=valid_payload
#     )
#     assert response.status_code == 404
#     assert response.json().get("error") == "STORE_NOT_FOUND"


# @pytest.mark.post  # tagging POST
# def test_delete_payment_offline_store_not_allowed():
#     response = requests.delete(
#         f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=1238",
#         headers={"Authorization": f"Bearer {admin_token}",
#                  "Content-Type": "application/json"},
#         json=valid_payload
#     )
#     assert response.status_code == 403
#     assert response.json().get("error") == "STORE_NOT_ALLOWED_ON_MERCHANT"


# @pytest.mark.post  # tagging POST
# def test_delete_payment_offline_empty_auth():
#     response = requests.delete(
#         f"{API_PORTAL_HOST}/api-payment/portal/v1/integration/payment/payment-offline?storeId=1238",
#         headers={"Authorization": "Bearer ",
#                  "Content-Type": "application/json"},
#         json=valid_payload
#     )
#     assert response.status_code == 401
#     assert response.json().get("error") == "Unauthorized"