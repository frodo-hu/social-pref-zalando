# api/routes/prefs.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db import get_db, OAuthToken
from ingestion.pinterest import PinterestClient
from preferences.preprocess import clean_caption
from preferences.feature_extractor import get_embedding
from rules_engine.engine import generate_layout_rules

router = APIRouter()

@router.get("/")
def get_preferences(db: Session = Depends(get_db)):
    # 1) load latest Pinterest token only
    pi_token = (
        db.query(OAuthToken)
          .filter_by(provider="pinterest")
          .order_by(OAuthToken.id.desc())
          .first()
    )

    # 2) fetch Pinterest pins (or empty)
    pi_pins = PinterestClient().get_pins(pi_token.access_token) if pi_token else []

    # 3) embed each pin’s image URL and cleaned caption
    embeddings: list[list[float]] = []
    for pin in pi_pins:
        # some pins embed media under different keys
        url = pin.get("media", {}).get("url") or pin.get("image", {}).get("url")
        if url:
            embeddings.append(get_embedding(url))

        # if Pinterest has any text/caption fields, clean & embed them too
        caption = clean_caption(pin.get("title", "") or pin.get("description", ""))
        if caption:
            embeddings.append(get_embedding(caption))

    # 4) prepare a small sample of Zalando products
    #    here we embed product names as proxies
    catalog_embeddings = {
        "nike-air-max-90":    get_embedding("nike air max 90"),
        "adidas-superstar":    get_embedding("adidas superstar"),
        "puma-rs-x":          get_embedding("puma rs x"),
        "newbalance-574":      get_embedding("new balance 574"),
        "reebok-club-c":       get_embedding("reebok club c"),
    }

    # 5) generate layout rules (handles empty embeddings gracefully)
    rules = generate_layout_rules(embeddings, catalog_embeddings)

    return rules