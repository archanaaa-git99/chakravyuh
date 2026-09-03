# tests/test_correlation.py

from datetime import date, datetime, timezone

from backend.models.case import Case
from backend.models.known_entity import KnownEntity
from backend.models.past_case import PastCase
from backend.models.wallet_trail import WalletInTrail
from backend.services.correlation import (
    check_known_entity,
    correlate_wallet,
    find_overlapping_active_cases,
    find_overlapping_past_cases,
)


def _make_case(db_session, case_number, wallet_address):
    case = Case(
        case_number=case_number,
        victim_name="Victim",
        complaint_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        origin_wallet_address=wallet_address,
        fraud_type="scam",
    )
    db_session.add(case)
    db_session.flush()

    wallet = WalletInTrail(case_id=case.id, wallet_address=wallet_address, hop_level=0)
    db_session.add(wallet)
    db_session.flush()

    return case, wallet


def test_find_overlapping_active_cases(db_session):
    case_a, _ = _make_case(db_session, "CASE-A", "0xSHARED")
    case_b, _ = _make_case(db_session, "CASE-B", "0xSHARED")
    db_session.commit()

    results = find_overlapping_active_cases(db_session, "0xSHARED", exclude_case_id=case_a.id)

    assert len(results) == 1
    assert results[0]["case_number"] == "CASE-B"


def test_find_overlapping_past_cases(db_session):
    past = PastCase(
        past_case_reference="OLD-001",
        wallet_address="0xHISTORY",
        fraud_type="ponzi_scheme",
        case_summary="Old case",
        date_closed=date(2024, 1, 1),
    )
    db_session.add(past)
    db_session.commit()

    results = find_overlapping_past_cases(db_session, "0xHISTORY")

    assert len(results) == 1
    assert results[0]["past_case_reference"] == "OLD-001"


def test_check_known_entity(db_session):
    entity = KnownEntity(
        wallet_address="0xMIXER",
        entity_name="Test Mixer",
        entity_type="mixer",
        risk_level="critical",
    )
    db_session.add(entity)
    db_session.commit()

    result = check_known_entity(db_session, "0xMIXER")

    assert result is not None
    assert result["entity_type"] == "mixer"


def test_correlate_wallet_combines_all_sources(db_session):
    case_a, _ = _make_case(db_session, "CASE-A", "0xFULLTEST")
    case_b, _ = _make_case(db_session, "CASE-B", "0xFULLTEST")

    past = PastCase(
        past_case_reference="OLD-002",
        wallet_address="0xFULLTEST",
        fraud_type="scam",
        date_closed=date(2023, 5, 5),
    )
    db_session.add(past)
    db_session.commit()

    result = correlate_wallet(db_session, "0xFULLTEST", exclude_case_id=case_a.id)

    assert result["has_overlap"] is True
    assert len(result["overlapping_active_cases"]) == 1
    assert result["overlapping_active_cases"][0]["case_number"] == "CASE-B"
    assert len(result["overlapping_past_cases"]) == 1


def test_correlate_wallet_no_match(db_session):
    result = correlate_wallet(db_session, "0xNOMATCH")

    assert result["has_overlap"] is False
    assert result["is_known_entity"] is False
