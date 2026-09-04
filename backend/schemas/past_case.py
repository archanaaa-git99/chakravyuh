# backend/schemas/past_case.py

from datetime import date

from pydantic import BaseModel, ConfigDict


class PastCaseBase(BaseModel):
    past_case_reference: str
    wallet_address: str
    fraud_type: str
    case_summary: str | None = None
    date_closed: date | None = None
    linked_case_id: int | None = None


class PastCaseCreate(PastCaseBase):
    pass


class PastCaseRead(PastCaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
