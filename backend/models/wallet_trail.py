# backend/models/wallet_trail.py

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.case import Case
    from backend.models.flag import Flag


class WalletInTrail(Base):
    __tablename__ = "wallets_in_trail"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True, nullable=False)
    wallet_address: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    hop_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    parent_wallet_id: Mapped[int | None] = mapped_column(
        ForeignKey("wallets_in_trail.id"), nullable=True
    )

    is_suspect_origin: Mapped[bool] = mapped_column(Boolean, default=False)
    discovered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    case: Mapped["Case"] = relationship(back_populates="wallets")
    parent: Mapped["WalletInTrail"] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list["WalletInTrail"]] = relationship(back_populates="parent")

    flags: Mapped[list["Flag"]] = relationship(back_populates="wallet")

    __table_args__ = (Index("ix_wallet_address_case_id", "wallet_address", "case_id"),)
