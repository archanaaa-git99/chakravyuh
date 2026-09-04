# backend/routers/correlation_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.correlation import correlate_case, correlate_wallet

router = APIRouter(prefix="/correlation", tags=["correlation"])


@router.get("/wallet/{wallet_address}")
def get_wallet_correlation(
    wallet_address: str,
    exclude_case_id: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Check a single wallet address for cross-case overlap,
    past-case matches, and known-entity matches.
    """
    return correlate_wallet(db, wallet_address, exclude_case_id)


@router.get("/case/{case_id}")
def get_case_correlation(case_id: int, db: Session = Depends(get_db)):
    """
    Run correlation for every wallet discovered in a given case.
    """
    return correlate_case(db, case_id)
