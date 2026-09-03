# backend/schemas/case.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CaseBase(BaseModel):
    case_number: str
    victim_name: str
    victim_contact: str | None = None
    complaint_date: datetime
    origin_wallet_address: str
    fraud_type: str
    status: str = "open"
    description: str | None = None


class CaseCreate(CaseBase):
    pass


class CaseRead(CaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
