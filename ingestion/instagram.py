# ingestion/instagram.py
import os
from requests_oauthlib import OAuth2Session

class InstagramClient:
    AUTH_URL   = "https://api.instagram.com/oauth/authorize"
    TOKEN_URL  = "https://api.instagram.com/oauth/access_token"
    GRAPH_BASE = "https://graph.instagram.com"

    def __init__(self):
        self.client_id     = os.getenv("INSTAGRAM_CLIENT_ID")
        self.client_secret = os.getenv("INSTAGRAM_CLIENT_SECRET")
        self.redirect_uri  = os.getenv("INSTAGRAM_REDIRECT_URI")
        self.session = OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=["user_profile","user_media"]
        )

    def get_authorize_url(self):
        url, _ = self.session.authorization_url(self.AUTH_URL)
        return url

    def fetch_token(self, full_response_url):
        token = self.session.fetch_token(
            token_url=self.TOKEN_URL,
            client_secret=self.client_secret,
            authorization_response=full_response_url
        )
        return token

    def get_media(self, access_token):
        resp = self.session.get(
            f"{self.GRAPH_BASE}/me/media",
            params={"fields":"id,caption,media_url","access_token":access_token}
        )
        return resp.json().get("data", [])