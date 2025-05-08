from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env at project root (explicit path)
project_root = Path(__file__).parent.parent
dotenv_path = project_root / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path, override=True)
    print("Loaded .env from:", dotenv_path)
else:
    print("Warning: .env file not found at", dotenv_path)

print("PINTEREST_SANDBOX_TOKEN:", os.getenv("PINTEREST_SANDBOX_TOKEN"))
print("PINTEREST_CLIENT_ID:", os.getenv("PINTEREST_CLIENT_ID"))
print("PINTEREST_REDIRECT_URI:", os.getenv("PINTEREST_REDIRECT_URI"))

from fastapi import FastAPI
from api.routes.users import router as users_router
from api.routes.prefs import router as prefs_router

# Create the FastAPI “app” that Uvicorn will look for
app = FastAPI(title="Social→Zalando Prototype")
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(prefs_router, prefix="/preferences", tags=["preferences"])

@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Hello from FastAPI 🚀"}