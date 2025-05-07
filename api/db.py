# api/db.py

import os
from dotenv import load_dotenv

# 1. load .env from project root
load_dotenv()

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 2. now this should pull from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in environment")

# 3. Create your engine & session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    """
    FastAPI dependency that provides a database session,
    and ensures it’s closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, index=True)
    access_token = Column(Text)
    refresh_token = Column(Text, nullable=True)
    expires_in = Column(Integer, nullable=True)

# 4. create tables
Base.metadata.create_all(bind=engine)