# api/main.py

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