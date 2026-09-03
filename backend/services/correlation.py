# backend/services/correlation.py

"""
Cross-case wallet overlap correlation logic.

Given a wallet address (or a case), this module finds:
  1. Other active cases that share the same wallet address.
  2. Past (closed) fraud cases that involved the same wallet address.
  3. Whether the wallet is a known entity (exchange, mixer, scammer, etc.)

This is intentionally a simple, direct equality-match query as scoped
for the MVP -- no fuzzy matching, no graph traversal beyond what's
already stored in wallets_in_trail.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.case import Case
from backend.models.known_entity import KnownEntity
from backend.models.past_case import PastCase
from backend.models.wallet_trail import WalletInTrail


def find_overlapping_active_cases(
    db: Session, wallet_address: str, exclude_case_id: int | None = None
) -> list[dict]:
    """
    Finds other ACTIVE cases (in wallets_in_trail) that contain the same
    wallet_address. Excludes the case you're currently investigating
    (exclude_case_id) so you don't match a wallet against its own case.
    """
    stmt = (
        select(WalletInTrail, Case)
        .join(Case, Case.id == WalletInTrail.case_id)
        .where(WalletInTrail.wallet_address == wallet_address)
    )

    if exclude_case_id is not None:
        stmt = stmt.where(WalletInTrail.case_id != exclude_case_id)

    results = db.execute(stmt).all()

    return [
        {
            "case_id": case.id,
            "case_number": case.case_number,
            "fraud_type": case.fraud_type,
            "status": case.status,
            "hop_level": wallet.hop_level,
            "wallet_id": wallet.id,
        }
        for wallet, case in results
    ]


def find_overlapping_past_cases(db: Session, wallet_address: str) -> list[dict]:
    """
    Finds records in past_cases where the wallet_address matches --
    i.e. this wallet was involved in a previously closed fraud case.
    """
    stmt = select(PastCase).where(PastCase.wallet_address == wallet_address)
    results = db.execute(stmt).scalars().all()

    return [
        {
            "past_case_id": pc.id,
            "past_case_reference": pc.past_case_reference,
            "fraud_type": pc.fraud_type,
            "case_summary": pc.case_summary,
            "date_closed": pc.date_closed,
        }
        for pc in results
    ]


def check_known_entity(db: Session, wallet_address: str) -> dict | None:
    """
    Checks if the wallet_address is a known entity
    (exchange, mixer, scammer, etc.).
    """
    stmt = select(KnownEntity).where(KnownEntity.wallet_address == wallet_address)
    entity = db.execute(stmt).scalar_one_or_none()

    if entity is None:
        return None

    return {
        "entity_name": entity.entity_name,
        "entity_type": entity.entity_type,
        "risk_level": entity.risk_level,
        "source": entity.source,
    }


def correlate_wallet(db: Session, wallet_address: str, exclude_case_id: int | None = None) -> dict:
    """
    Master correlation function -- runs all three checks for a single
    wallet address and returns a combined result. This is the main
    entry point other modules / routes should call.
    """
    overlapping_cases = find_overlapping_active_cases(db, wallet_address, exclude_case_id)
    past_case_matches = find_overlapping_past_cases(db, wallet_address)
    known_entity = check_known_entity(db, wallet_address)

    return {
        "wallet_address": wallet_address,
        "has_overlap": bool(overlapping_cases) or bool(past_case_matches),
        "is_known_entity": known_entity is not None,
        "overlapping_active_cases": overlapping_cases,
        "overlapping_past_cases": past_case_matches,
        "known_entity_details": known_entity,
    }


def correlate_case(db: Session, case_id: int) -> list[dict]:
    """
    Runs correlate_wallet() for every wallet discovered in a given case's
    trail. Returns a list of correlation results, one per wallet.
    Useful for a full "correlate this whole case" investigator action.
    """
    stmt = select(WalletInTrail).where(WalletInTrail.case_id == case_id)
    wallets = db.execute(stmt).scalars().all()

    return [
        correlate_wallet(db, wallet.wallet_address, exclude_case_id=case_id) for wallet in wallets
    ]
