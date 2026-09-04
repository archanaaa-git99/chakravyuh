from fastapi import FastAPI

from backend.config import settings
from backend.database import init_db
from backend.routers.correlation_router import router as correlation_router
from backend.services.blockchain_service import get_wallet_transactions
from backend.routers.blockchain_router import router as blockchain_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(correlation_router)
app.include_router(blockchain_router)


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


@app.get("/wallet/{wallet_address}/transactions")
def wallet_transactions(wallet_address: str):
    return get_wallet_transactions(wallet_address)