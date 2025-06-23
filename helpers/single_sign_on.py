import os
import json
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv  # Equivalent to your JS posPage.postLogin()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger()

# Load environment variables
load_dotenv()

ENV = os.getenv("ENV")
API_POS = os.getenv("API_POS")

if ENV != "prod":
    API_POS_HOST = f"https://{ENV}-{API_POS}"
else:
    API_POS_HOST = f"https://{API_POS}"

# File paths
BASE_DIR = Path(__file__).resolve().parent
LOGIN_DATA_PATH = BASE_DIR / "../fixtures/data/login_data.json"
ADMIN_TOKEN_PATH = BASE_DIR / "../fixtures/admin_token.json"
SUPER_ADMIN_TOKEN_PATH = BASE_DIR / "../fixtures/super_admin_token.json"

# Load login data
with open(LOGIN_DATA_PATH, "r", encoding="utf-8") as file:
    login_data = json.load(file)

admin_tokens = {}
super_admin_tokens = {}


def login_to_portal_as_admin():
    try:
        env = os.getenv("ENV")
        password = os.getenv("PASSWORD")

        if env not in login_data.get("adminAccounts", {}):
            raise ValueError(f"❌ There are no accounts on ENV {env}")

        email = login_data.get("adminEmail")

        if not email or not password:
            log.error(f"❌ Missing credentials for admin in {env}.")
            return

        log.info("🔄 Generating admin token in progress...")

        response = requests.post(f"{API_POS_HOST}/api/oauth/v2/idepos/login",
                                 json={"email": email, "password": password})

        if response.status_code == 200:
            admin_tokens[env] = response.json()["data"]["authKey"]

            with open(ADMIN_TOKEN_PATH, "w", encoding="utf-8") as f:
                json.dump(admin_tokens, f, indent=2)

            log.info(f"✅ Admin token in {env} successfully generated")
        else:
            error_message = response.json().get(
                "message") or response.json().get("error") or "Unknown error"
            raise ValueError(f"❌ Login admin failed in {env}: {error_message}")
        return admin_tokens

    except Exception as error:
        log.error(f"❌ Error logging in as admin: {error}")
        raise


def login_to_portal_as_super_admin():
    try:
        env = os.getenv("ENV")
        password = os.getenv("PASSWORD")

        if env == "prod":
            return

        email = login_data.get("superAdminEmail")

        if not email or not password:
            log.error(f"❌ Missing credentials for super admin in {env}.")
            return

        log.info("🔄 Generating super admin token in progress...")

        response = requests.post(f"{API_POS_HOST}/api/oauth/v2/idepos/login",
                                 json={"email": email, "password": password})

        if response.status_code == 200:
            super_admin_tokens[env] = response.json()["data"]["authKey"]

            with open(SUPER_ADMIN_TOKEN_PATH, "w", encoding="utf-8") as f:
                json.dump(super_admin_tokens, f, indent=2)

            log.info(f"✅ Super admin token in {env} successfully generated")
        else:
            error_message = response.json().get(
                "message") or response.json().get("error") or "Unknown error"
            raise ValueError(
                f"❌ Login super admin failed in {env}: {error_message}")
        return super_admin_tokens

    except Exception as error:
        log.error(f"❌ Error logging in as super admin: {error}")
        raise


if __name__ == "__main__":
    login_to_portal_as_admin()
    login_to_portal_as_super_admin()
