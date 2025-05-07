'''
# preferences/feature_extractor.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str) -> list[float]:
    """
    Embed any piece of text (or a textual proxy for an image) via OpenAI’s text-embedding-ada-002.
    """
    resp = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp["data"][0]["embedding"]
'''

# preferences/feature_extractor.py

import numpy as np

def get_embedding(text: str) -> list[float]:
    """
    Dummy embedding: returns a fixed-size random vector.
    Used to avoid rate limits during prototype.
    """
    # Seed for reproducibility (optional)
    # np.random.seed(hash(text) % (2**32))
    return np.random.rand(512).tolist()