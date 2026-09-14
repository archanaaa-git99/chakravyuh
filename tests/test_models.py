# tests/test_models.py

from datetime import datetime, timezone

from backend.models.case import Case
from backend.models.flag import Flag
from backend.models.known_entity import KnownEntity
from backend.models.transaction import Transaction
from backend.models.wallet_trail import WalletInTrail


def test_create_case(db_session):
    case = Case(
        case_number="TEST-0001",
        victim_name="Test Victim",
        complaint_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        origin_wallet_address="0xTEST",
        fraud_type="phishing",
    )
    db_session.add(case)
    db_session.commit()

    assert case.id is not None
    assert case.status == "open"


def test_wallet_trail_self_reference(db_session):
    case = Case(
        case_number="TEST-0002",
        victim_name="Test Victim 2",
        complaint_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        origin_wallet_address="0xORIGIN",
        fraud_type="scam",
    )
    db_session.add(case)
    db_session.flush()

    parent_wallet = WalletInTrail(case_id=case.id, wallet_address="0xORIGIN", hop_level=0)
    db_session.add(parent_wallet)
    db_session.flush()

    child_wallet = WalletInTrail(
        case_id=case.id,
        wallet_address="0xHOP1",
        hop_level=1,
        parent_wallet_id=parent_wallet.id,
    )
    db_session.add(child_wallet)
    db_session.commit()

    assert child_wallet.parent_wallet_id == parent_wallet.id
    assert child_wallet.parent.wallet_address == "0xORIGIN"


def test_transaction_links_two_wallets(db_session):
    case = Case(
        case_number="TEST-0003",
        victim_name="Test Victim 3",
        complaint_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        origin_wallet_address="0xA",
        fraud_type="scam",
    )
    db_session.add(case)
    db_session.flush()

    wallet_a = WalletInTrail(case_id=case.id, wallet_address="0xA", hop_level=0)
    wallet_b = WalletInTrail(case_id=case.id, wallet_address="0xB", hop_level=1)
    db_session.add_all([wallet_a, wallet_b])
    db_session.flush()

    txn = Transaction(
        case_id=case.id,
        from_wallet_id=wallet_a.id,
        to_wallet_id=wallet_b.id,
        amount=1.5,
        currency="BTC",
        hop_level=1,
        timestamp=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )
    db_session.add(txn)
    db_session.commit()

    assert txn.from_wallet.wallet_address == "0xA"
    assert txn.to_wallet.wallet_address == "0xB"


def test_known_entity_unique_wallet(db_session):
    entity = KnownEntity(
        wallet_address="0xMIXER",
        entity_name="Test Mixer",
        entity_type="mixer",
        risk_level="high",
    )
    db_session.add(entity)
    db_session.commit()

    assert entity.id is not None


def test_flag_links_case_and_wallet(db_session):
    case = Case(
        case_number="TEST-0004",
        victim_name="Test Victim 4",
        complaint_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
        origin_wallet_address="0xFLAGTEST",
        fraud_type="scam",
    )
    db_session.add(case)
    db_session.flush()

    wallet = WalletInTrail(case_id=case.id, wallet_address="0xFLAGTEST", hop_level=0)
    db_session.add(wallet)
    db_session.flush()

    flag = Flag(
        case_id=case.id,
        wallet_id=wallet.id,
        flag_type="high_velocity",
        severity="medium",
        description="Rapid fund movement detected.",
    )
    db_session.add(flag)
    db_session.commit()

    assert flag.wallet.wallet_address == "0xFLAGTEST"
