# ingestion/pinterest.py

import os
import requests
from urllib.parse import urlencode

print("PINTEREST_CLIENT_ID:", os.getenv("PINTEREST_CLIENT_ID"))
print("PINTEREST_REDIRECT_URI:", os.getenv("PINTEREST_REDIRECT_URI"))
print("PINTEREST_SANDBOX_TOKEN:", os.getenv("PINTEREST_SANDBOX_TOKEN"))

class PinterestClient:
    AUTH_URL     = "https://api.pinterest.com/oauth/"
    TOKEN_URL    = "https://api.pinterest.com/v5/oauth/token"
    API_BASE     = "https://api.pinterest.com/v5"
    V1_ME_PINS   = "https://api.pinterest.com/v1/me/pins/"

    def __init__(self, token: str = None):
        # Prefer passed-in token, else sandbox token from env
        self.client_id     = os.getenv("PINTEREST_CLIENT_ID")
        self.client_secret = os.getenv("PINTEREST_CLIENT_SECRET")
        self.redirect_uri  = os.getenv("PINTEREST_REDIRECT_URI")
        self.sandbox_token = os.getenv("PINTEREST_SANDBOX_TOKEN")
        self.token         = token or self.sandbox_token

    def get_authorize_url(self) -> str:
        params = {
            "response_type": "code",
            "client_id":     self.client_id,
            "redirect_uri":  self.redirect_uri,
            "scope":         "pins:read boards:read user_accounts:read",
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    def fetch_token(self, code: str) -> dict:
        data = {
            "grant_type":    "authorization_code",
            "code":          code,
            "client_id":     self.client_id,
            "client_secret": self.client_secret,
        }
        resp = requests.post(self.TOKEN_URL, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_pins(self, access_token: str = None) -> list:
        # Decide which token to use
        token = access_token or self.token
        if not token:
            raise RuntimeError("No Pinterest access token available")

        try:
            # Sandbox tokens only work on the v1 pins endpoint
            if token == self.sandbox_token:
                url = f"{self.V1_ME_PINS}?access_token={token}"
                resp = requests.get(url)
            else:
                headers = {"Authorization": f"Bearer {token}"}
                resp = requests.get(f"{self.API_BASE}/users/me/pins", headers=headers)

            resp.raise_for_status()
            data = resp.json()
            # both v1 and v5 wrap results under "data"
            return data.get("data", [])
        except Exception as e:
            # avoid 502’s downstream
            print("❌ PinterestClient.get_pins failed:", repr(e))
            return []