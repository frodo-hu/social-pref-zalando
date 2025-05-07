# preferences/preprocess.py

import re

def clean_caption(caption: str) -> str:
    """
    Lowercase, remove URLs/mentions/extra whitespace.
    """
    text = caption.lower()
    text = re.sub(r'https?://\S+', '', text)        # drop URLs
    text = re.sub(r'[@#]\w+', '', text)             # drop @mentions and #tags
    text = re.sub(r'[^a-z0-9\s]', '', text)         # keep only alphanumeric+space
    text = re.sub(r'\s+', ' ', text).strip()        # collapse whitespace
    return text