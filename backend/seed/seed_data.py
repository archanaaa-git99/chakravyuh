# backend/seed/seed_data.py

"""
Seeds the database with fictional demo data for CHAKRAVYUH.

Scenario designed to actually exercise correlation.py:
  - Case A and Case B share a wallet (cross-case overlap).
  - One wallet in Case A also appears in past_cases (historical match).
  - One wallet is a known mixer (known_entities match).

Run this file directly:  python -m backend.seed.seed_data
"""

from datetime import date, datetime, timezone

from backend.database import SessionLocal, init_db
from backend.models.case import Case
from backend.models.flag import Flag
from backend.models.known_entity import KnownEntity
from backend.models.past_case import PastCase
from backend.models.transaction import Transaction
from backend.models.wallet_trail import WalletInTrail


def seed():
    init_db()
    db = SessionLocal()

    try:
        # ---------- CASES ----------
        case_a = Case(
            case_number="CHK-2026-0001",
            victim_name="Ramesh Gupta",
            victim_contact="ramesh.gupta@example.com",
            complaint_date=datetime(2026, 8, 1, 10, 30, tzinfo=timezone.utc),
            origin_wallet_address="0xAAA111VICTIM",
            fraud_type="investment_scam",
            status="investigating",
            description="Victim invested in a fake crypto trading platform.",
        )

        case_b = Case(
            case_number="CHK-2026-0002",
            victim_name="Sunita Rao",
            victim_contact="sunita.rao@example.com",
            complaint_date=datetime(2026, 8, 15, 14, 0, tzinfo=timezone.utc),
            origin_wallet_address="0xBBB222VICTIM",
            fraud_type="phishing",
            status="open",
            description="Victim's wallet drained via phishing link.",
        )

        db.add_all([case_a, case_b])
        db.flush()  # get IDs without full commit

        # ---------- WALLETS IN TRAIL (Case A) ----------
        wallet_a0 = WalletInTrail(
            case_id=case_a.id,
            wallet_address="0xAAA111VICTIM",
            hop_level=0,
            is_suspect_origin=True,
        )
        db.add(wallet_a0)
        db.flush()

        wallet_a1 = WalletInTrail(
            case_id=case_a.id,
            wallet_address="0xSHARED999",  # <-- shared with Case B
            hop_level=1,
            parent_wallet_id=wallet_a0.id,
        )
        db.add(wallet_a1)
        db.flush()

        wallet_a2 = WalletInTrail(
            case_id=case_a.id,
            wallet_address="0xMIXERKNOWN777",  # <-- known entity
            hop_level=2,
            parent_wallet_id=wallet_a1.id,
        )
        db.add(wallet_a2)
        db.flush()

        # ---------- WALLETS IN TRAIL (Case B) ----------
        wallet_b0 = WalletInTrail(
            case_id=case_b.id,
            wallet_address="0xBBB222VICTIM",
            hop_level=0,
            is_suspect_origin=True,
        )
        db.add(wallet_b0)
        db.flush()

        wallet_b1 = WalletInTrail(
            case_id=case_b.id,
            wallet_address="0xSHARED999",  # <-- same wallet as Case A hop 1
            hop_level=1,
            parent_wallet_id=wallet_b0.id,
        )
        db.add(wallet_b1)
        db.flush()

        # ---------- TRANSACTIONS ----------
        txn_a1 = Transaction(
            case_id=case_a.id,
            from_wallet_id=wallet_a0.id,
            to_wallet_id=wallet_a1.id,
            tx_hash="0xTXHASH_A1",
            amount=2.5,
            currency="BTC",
            hop_level=1,
            timestamp=datetime(2026, 8, 2, 9, 0, tzinfo=timezone.utc),
            is_suspicious=False,
        )

        txn_a2 = Transaction(
            case_id=case_a.id,
            from_wallet_id=wallet_a1.id,
            to_wallet_id=wallet_a2.id,
            tx_hash="0xTXHASH_A2",
            amount=2.4,
            currency="BTC",
            hop_level=2,
            timestamp=datetime(2026, 8, 3, 11, 0, tzinfo=timezone.utc),
            is_suspicious=True,
        )

        txn_b1 = Transaction(
            case_id=case_b.id,
            from_wallet_id=wallet_b0.id,
            to_wallet_id=wallet_b1.id,
            tx_hash="0xTXHASH_B1",
            amount=1.1,
            currency="ETH",
            hop_level=1,
            timestamp=datetime(2026, 8, 16, 8, 0, tzinfo=timezone.utc),
            is_suspicious=False,
        )

        db.add_all([txn_a1, txn_a2, txn_b1])

        # ---------- PAST CASES ----------
        past_case_1 = PastCase(
            past_case_reference="OLD-2024-0099",
            wallet_address="0xSHARED999",  # matches current wallet -> historical hit
            fraud_type="ponzi_scheme",
            case_summary="Closed case involving a ponzi scheme ring.",
            date_closed=date(2024, 11, 20),
        )
        db.add(past_case_1)

        # ---------- KNOWN ENTITIES ----------
        known_mixer = KnownEntity(
            wallet_address="0xMIXERKNOWN777",
            entity_name="ShadowMix Tumbler",
            entity_type="mixer",
            risk_level="critical",
            source="internal_watchlist",
            notes="Known mixing service used to obscure fund trails.",
        )
        db.add(known_mixer)

        db.flush()

        # ---------- FLAGS ----------
        flag_1 = Flag(
            case_id=case_a.id,
            wallet_id=wallet_a2.id,
            transaction_id=txn_a2.id,
            flag_type="known_mixer",
            severity="high",
            description="Funds routed through a known mixing service.",
        )
        db.add(flag_1)

        db.commit()
        print("Seed data inserted successfully.")
        print(f"   Case A: {case_a.case_number} (id={case_a.id})")
        print(f"   Case B: {case_b.case_number} (id={case_b.id})")
        print("   Shared wallet 0xSHARED999 links Case A <-> Case B")
        print("   Wallet 0xSHARED999 also appears in past_cases (OLD-2024-0099)")
        print("   Wallet 0xMIXERKNOWN777 is a known_entity (mixer)")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
