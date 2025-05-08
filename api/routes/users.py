# api/routes/users.py

import os
import requests
from fastapi import APIRouter, Depends, Request, HTTPException
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

# --- Instagram unchanged ---
@router.get("/auth/instagram")
def instagram_login():
    client = InstagramClient()
    return RedirectResponse(client.get_authorize_url())

@router.get("/auth/instagram/callback")
def instagram_callback(request: Request, db: Session = Depends(get_db)):
    client = InstagramClient()
    full_url = str(request.url)
    token_data = client.fetch_token(full_url)
    db_token = OAuthToken(
        provider="instagram",
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
    )
    db.add(db_token)
    db.commit()
    return {"message": "Instagram token saved."}

# --- Pinterest with sandbox shortcut ---
@router.get("/auth/pinterest")
def pinterest_login(db: Session = Depends(get_db)):
    sandbox = os.getenv("PINTEREST_SANDBOX_TOKEN")
    if sandbox:
        # Save sandbox token directly
        db_token = OAuthToken(provider="pinterest", access_token=sandbox)
        db.add(db_token)
        db.commit()
        return {"message": "Using sandbox Pinterest token."}

    # Otherwise kick off real OAuth
    client = PinterestClient()
    return RedirectResponse(client.get_authorize_url())

@router.get("/auth/pinterest/callback")
def pinterest_callback(code: str, db: Session = Depends(get_db)):
    client = PinterestClient()
    token_data = client.fetch_token(code)
    if "access_token" not in token_data:
        raise HTTPException(400, detail="Failed to fetch Pinterest token")
    db_token = OAuthToken(
        provider="pinterest",
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
    )
    db.add(db_token)
    db.commit()
    return {"message": "Pinterest token saved."}