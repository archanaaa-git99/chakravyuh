from fastapi import APIRouter, HTTPException

from backend.services.blockchain_service import (
    get_wallet_transactions,
)

router = APIRouter(
    prefix="/wallet",
    tags=["Blockchain"],
)


@router.get("/{wallet_address}/transactions")
def wallet_transactions(
    wallet_address: str,
    page: int = 1,
    offset: int = 100,
):
    try:
        return get_wallet_transactions(
            wallet_address,
            page=page,
            offset=offset,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error