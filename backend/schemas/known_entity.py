# backend/schemas/known_entity.py

from pydantic import BaseModel, ConfigDict


class KnownEntityBase(BaseModel):
    wallet_address: str
    entity_name: str
    entity_type: str
    risk_level: str = "low"
    source: str | None = None
    notes: str | None = None


class KnownEntityCreate(KnownEntityBase):
    pass


class KnownEntityRead(KnownEntityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
