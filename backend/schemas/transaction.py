# backend/schemas/transaction.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    case_id: int
    from_wallet_id: int
    to_wallet_id: int
    tx_hash: str | None = None
    amount: float
    currency: str = "BTC"
    hop_level: int = 0
    timestamp: datetime
    is_suspicious: bool = False


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
