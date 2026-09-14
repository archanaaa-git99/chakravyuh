# backend/models/transaction.py

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.case import Case
    from backend.models.flag import Flag
    from backend.models.wallet_trail import WalletInTrail


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True, nullable=False)

    from_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets_in_trail.id"), index=True, nullable=False
    )
    to_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets_in_trail.id"), index=True, nullable=False
    )

    tx_hash: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(20), nullable=False, default="BTC")
    hop_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_suspicious: Mapped[bool] = mapped_column(Boolean, default=False)

    case: Mapped["Case"] = relationship(back_populates="transactions")
    from_wallet: Mapped["WalletInTrail"] = relationship(foreign_keys=[from_wallet_id])
    to_wallet: Mapped["WalletInTrail"] = relationship(foreign_keys=[to_wallet_id])

    flags: Mapped[list["Flag"]] = relationship(back_populates="transaction")
