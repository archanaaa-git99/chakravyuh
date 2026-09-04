# backend/models/past_case.py

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base

if TYPE_CHECKING:
    from backend.models.case import Case


class PastCase(Base):
    __tablename__ = "past_cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    past_case_reference: Mapped[str] = mapped_column(String(100), nullable=False)
    wallet_address: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    fraud_type: Mapped[str] = mapped_column(String(100), nullable=False)
    case_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_closed: Mapped[date | None] = mapped_column(Date, nullable=True)

    linked_case_id: Mapped[int | None] = mapped_column(ForeignKey("cases.id"), nullable=True)

    linked_case: Mapped["Case"] = relationship()
