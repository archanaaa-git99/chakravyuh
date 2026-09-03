# backend/models/flag.py

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.case import Case
    from backend.models.transaction import Transaction
    from backend.models.wallet_trail import WalletInTrail


class Flag(Base):
    __tablename__ = "flags"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True, nullable=False)
    wallet_id: Mapped[int | None] = mapped_column(
        ForeignKey("wallets_in_trail.id"), index=True, nullable=True
    )
    transaction_id: Mapped[int | None] = mapped_column(ForeignKey("transactions.id"), nullable=True)

    flag_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="low")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    case: Mapped["Case"] = relationship(back_populates="flags")
    wallet: Mapped["WalletInTrail"] = relationship(back_populates="flags")
    transaction: Mapped["Transaction"] = relationship(back_populates="flags")
