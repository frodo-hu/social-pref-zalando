# api/routes/prefs.py

from typing import List, Dict, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db, OAuthToken
from ingestion.pinterest import PinterestClient
from preferences.preprocess import clean_caption
from preferences.feature_extractor import get_embedding
from rules_engine.engine import generate_layout_rules

router = APIRouter()

@router.get("/")
def get_preferences(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
):
    # 1) Pick up token from header or fall back to DB
    token: Optional[str] = None
    if authorization:
        if not authorization.lower().startswith("bearer "):
            raise HTTPException(status_code=400, detail="Invalid Authorization header")
        token = authorization.split(" ", 1)[1].strip()

    if not token:
        db_token = (
            db.query(OAuthToken)
              .filter_by(provider="pinterest")
              .order_by(OAuthToken.id.desc())
              .first()
        )
        token = db_token.access_token if db_token else None

    if not token:
        raise HTTPException(status_code=401, detail="No Pinterest token provided")

    # 2) Fetch Pinterest pins
    try:
        pi_pins = PinterestClient().get_pins(token)
    except Exception as e:
        print("❌ PinterestClient.get_pins error:", repr(e))
        raise HTTPException(status_code=502, detail="Error fetching pins")

    # 3) Build user embeddings
    user_embeddings: List[List[float]] = []
    for pin in pi_pins:
        url = pin.get("media", {}).get("url") or pin.get("image", {}).get("url")
        if url:
            user_embeddings.append(get_embedding(url))
        caption = clean_caption(pin.get("title", "") or pin.get("description", ""))
        if caption:
            user_embeddings.append(get_embedding(caption))

    # **NEW**: if we got no embeddings, return a “no-prefs” default
    if not user_embeddings:
        return {
            "highlightProducts": [],
            "themeColors": {
                "primary": "#ff0000",
                "secondary": "#0000ff"
            }
        }

    # 4) Sample catalog embeddings
    catalog_embeddings: Dict[str, List[float]] = {
        "nike-air-max-90":  get_embedding("nike air max 90"),
        "adidas-superstar": get_embedding("adidas superstar"),
        "puma-rs-x":        get_embedding("puma rs x"),
        "newbalance-574":   get_embedding("new balance 574"),
        "reebok-club-c":    get_embedding("reebok club c"),
    }

    # 5) Generate layout rules
    rules = generate_layout_rules(user_embeddings, catalog_embeddings)
    return rules