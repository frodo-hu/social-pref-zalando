# api/routes/users.py
import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.db import SessionLocal, OAuthToken
from ingestion.instagram import InstagramClient
from ingestion.pinterest import PinterestClient

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Instagram ---
@router.get("/auth/instagram")
def instagram_login():
    client = InstagramClient()
    return RedirectResponse(client.get_authorize_url())

@router.get("/auth/instagram/callback")
def instagram_callback(request: Request, db: Session = Depends(get_db)):
    client = InstagramClient()
    full_url = str(request.url)
    token_data = client.fetch_token(full_url)
    # save token in DB:
    db_token = OAuthToken(
        provider="instagram",
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in")
    )
    db.add(db_token)
    db.commit()
    return {"message":"Instagram token saved."}

# --- Pinterest ---
@router.get("/auth/pinterest")
def pinterest_login():
    client = PinterestClient()
    return RedirectResponse(client.get_authorize_url())

@router.get("/auth/pinterest/callback")
def pinterest_callback(code: str, db: Session = Depends(get_db)):
    client = PinterestClient()
    token_data = client.fetch_token(code)
    db_token = OAuthToken(
        provider="pinterest",
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in")
    )
    db.add(db_token)
    db.commit()
    return {"message":"Pinterest token saved."}