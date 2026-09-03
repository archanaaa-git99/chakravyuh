# backend/schemas/flag.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FlagBase(BaseModel):
    case_id: int
    wallet_id: int | None = None
    transaction_id: int | None = None
    flag_type: str
    severity: str = "low"
    description: str | None = None


class FlagCreate(FlagBase):
    pass


class FlagRead(FlagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
