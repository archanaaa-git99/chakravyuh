# CHAKRAVYUH — Database Schema & Integration Guide

Owned by: Member 4 (Database + Cross-Case Correlation)

This document explains the database layer so other team members can
read/write data correctly without needing to read the model source code.

---

## Tech Stack

- SQLite (MVP) via SQLAlchemy 2.x
- Database file created automatically: `chakravyuh.db`
- All models: `backend/models/`

---

## How to import and use the models

```python
from backend.database import SessionLocal
from backend.models.case import Case
from backend.models.wallet_trail import WalletInTrail
from backend.models.transaction import Transaction
from backend.models.past_case import PastCase
from backend.models.known_entity import KnownEntity
from backend.models.flag import Flag

db = SessionLocal()
```

Always close the session when done (`db.close()`), or use it as a
FastAPI dependency via `backend.database.get_db`.

---

## Table Reference

### `cases`
One row per victim complaint / investigation.

| Column | Type | Notes |
|---|---|---|
| id | int (PK) | |
| case_number | str, unique | e.g. `CHK-2026-0001` |
| victim_name | str | |
| victim_contact | str, nullable | |
| complaint_date | datetime | |
| origin_wallet_address | str | victim's reported wallet (hop 0) |
| fraud_type | str | e.g. `investment_scam`, `phishing` |
| status | str | `open`, `investigating`, `closed` |
| description | str, nullable | |
| created_at / updated_at | datetime | auto-managed |

---

### `wallets_in_trail`
Every wallet discovered while tracing a case, up to 3 hops.
**Member 3 (Tracer) should write to this table** as new wallets are
discovered during hop-tracing.

| Column | Type | Notes |
|---|---|---|
| id | int (PK) | |
| case_id | int (FK → cases.id) | |
| wallet_address | str | **indexed** — used for correlation |
| hop_level | int | 0 = origin, 1–3 = hops |
| parent_wallet_id | int, nullable (FK → wallets_in_trail.id) | builds the hop tree |
| is_suspect_origin | bool | |
| discovered_at | datetime | auto-set |
| notes | str, nullable | |

**Example — adding a newly discovered wallet (for Member 3's tracer):**
```python
new_wallet = WalletInTrail(
    case_id=case.id,
    wallet_address="0xNEWWALLET123",
    hop_level=1,
    parent_wallet_id=parent_wallet.id,
)
db.add(new_wallet)
db.commit()
```

---

### `transactions`
Money movements between wallets in a case's trail.
**Member 2 (Blockchain) / Member 3 (Tracer) write here** as they fetch
real transaction data.

| Column | Type | Notes |
|---|---|---|
| id | int (PK) | |
| case_id | int (FK → cases.id) | |
| from_wallet_id | int (FK → wallets_in_trail.id) | |
| to_wallet_id | int (FK → wallets_in_trail.id) | |
| tx_hash | str, nullable | blockchain transaction hash |
| amount | float | |
| currency | str | e.g. `BTC`, `ETH` |
| hop_level | int | |
| timestamp | datetime | |
| is_suspicious | bool | set by Member 3's rule engine |

---

### `past_cases`
Lightweight historical record used for correlation matching only.

| Column | Type | Notes |
|---|---|---|
| id | int (PK) | |
| past_case_reference | str | old case label |
| wallet_address | str | **indexed** |
| fraud_type | str | |
| case_summary | str, nullable | |
| date_closed | date, nullable | |
| linked_case_id | int, nullable (FK → cases.id) | |

---

### `known_entities`
Static lookup — exchanges, mixers, known scam wallets.
**Member 3 (rule engine / "known risky-address rule") should query this
table** rather than maintaining a separate list.

| Column | Type | Notes |
|---|---|---|
| id | int (PK) | |
| wallet_address | str, unique | |
| entity_name | str | e.g. "Binance Hot Wallet" |
| entity_type | str | `exchange`, `mixer`, `scammer`, `individual`, `unknown` |
| risk_level | str | `low`, `medium`, `high`, `critical` |
| source | str, nullable | |
| notes | str, nullable | |

---

### `flags`
Suspicious-activity markers raised on a wallet or transaction.
**Member 3's rule engine should write here** whenever a rule fires.

| Column | Type | Notes |
|---|---|---|
| id | int (PK) | |
| case_id | int (FK → cases.id) | |
| wallet_id | int, nullable (FK → wallets_in_trail.id) | |
| transaction_id | int, nullable (FK → transactions.id) | |
| flag_type | str | e.g. `known_mixer`, `cross_case_overlap`, `high_velocity` |
| severity | str | `low`, `medium`, `high` |
| description | str, nullable | |
| created_at | datetime | auto-set |

---

## Cross-Case Correlation — `backend/services/correlation.py`

Main function other members should call:

```python
from backend.services.correlation import correlate_wallet

result = correlate_wallet(db, wallet_address="0xABC123", exclude_case_id=current_case_id)
```

**Returns:**
```python
{
    "wallet_address": "0xABC123",
    "has_overlap": True,
    "is_known_entity": False,
    "overlapping_active_cases": [{...}, {...}],
    "overlapping_past_cases": [{...}],
    "known_entity_details": None,
}
```

Also available:
- `correlate_case(db, case_id)` — runs correlation for every wallet in a case at once.

---

## API Endpoints (for frontend integration)

Base URL when running locally: `http://127.0.0.1:8000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/correlation/wallet/{wallet_address}` | Correlate a single wallet |
| GET | `/correlation/case/{case_id}` | Correlate every wallet in a case |

---

## Seed / Demo Data

```bash
python -m backend.seed.seed_data
```

Creates two linked cases sharing a wallet, plus a past-case match and a
known-mixer match — useful for demoing correlation without real blockchain data.

---

## What's NOT included here (owned by other members)

- Blockchain data fetching (Member 2)
- 3-hop tracing algorithm (Member 3)
- Report generation (Member 6)