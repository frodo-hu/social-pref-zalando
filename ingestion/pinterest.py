# ingestion/pinterest.py
import os, requests
from urllib.parse import urlencode
print("PINTEREST_CLIENT_ID:", os.getenv("PINTEREST_CLIENT_ID"))
print("PINTEREST_REDIRECT_URI:", os.getenv("PINTEREST_REDIRECT_URI"))

class PinterestClient:
    AUTH_URL = "https://api.pinterest.com/oauth/"
    TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
    API_BASE = "https://api.pinterest.com/v5"

    def __init__(self):
        self.client_id     = os.getenv("PINTEREST_CLIENT_ID")
        self.client_secret = os.getenv("PINTEREST_CLIENT_SECRET")
        self.redirect_uri  = os.getenv("PINTEREST_REDIRECT_URI")

    def get_authorize_url(self):
        params = {
            "response_type":"code",
            "client_id":self.client_id,
            "redirect_uri":self.redirect_uri,
            "scope":"pins:read boards:read"
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def fetch_token(self, code):
        data = {
            "grant_type":"authorization_code",
            "code":code,
            "client_id":self.client_id,
            "client_secret":self.client_secret,
        }
        resp = requests.post(self.TOKEN_URL, json=data)
        return resp.json()

    def get_pins(self, access_token):
        headers = {"Authorization":f"Bearer {access_token}"}
        resp = requests.get(f"{self.API_BASE}/users/me/pins", headers=headers)
        return resp.json().get("data", [])