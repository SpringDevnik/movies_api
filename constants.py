import os

from dotenv import load_dotenv

load_dotenv()

AUTH_API_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
MOVIES_API_BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

BASE_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

SUPER_ADMIN_CREDS = {
    "login": os.getenv("SUPER_ADMIN_LOGIN"),
    "password": os.getenv("SUPER_ADMIN_PASSWORD")
}
