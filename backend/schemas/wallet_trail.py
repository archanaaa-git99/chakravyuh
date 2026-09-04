# backend/schemas/wallet_trail.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WalletInTrailBase(BaseModel):
    case_id: int
    wallet_address: str
    hop_level: int = 0
    parent_wallet_id: int | None = None
    is_suspect_origin: bool = False
    notes: str | None = None


class WalletInTrailCreate(WalletInTrailBase):
    pass


class WalletInTrailRead(WalletInTrailBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    discovered_at: datetime
