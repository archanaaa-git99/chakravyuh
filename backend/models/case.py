# backend/models/case.py

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.flag import Flag
    from backend.models.transaction import Transaction
    from backend.models.wallet_trail import WalletInTrail


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    case_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    victim_name: Mapped[str] = mapped_column(String(150), nullable=False)
    victim_contact: Mapped[str | None] = mapped_column(String(150), nullable=True)
    complaint_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    origin_wallet_address: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    fraud_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    wallets: Mapped[list["WalletInTrail"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )
    flags: Mapped[list["Flag"]] = relationship(back_populates="case", cascade="all, delete-orphan")
