# backend/main.py

from fastapi import FastAPI

from backend.config import settings
from backend.database import init_db
from backend.routers.correlation_router import router as correlation_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(correlation_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {
        "message": "CHAKRAVYUH backend is running",
        "module": "Database + Cross-Case Correlation",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
