# CHAKRAVYUH — Database + Cross-Case Correlation Module

This module (Member 4) provides the database layer and cross-case wallet
correlation logic for CHAKRAVYUH, a cryptocurrency fraud investigation
platform built for Smart India Hackathon.

## Responsibilities

- Database setup (SQLAlchemy 2.x + SQLite for MVP)
- Six core tables: `cases`, `transactions`, `wallets_in_trail`,
  `past_cases`, `known_entities`, `flags`
- Fictional demo data seeding
- Cross-case wallet overlap correlation (`backend/services/correlation.py`)

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x (typed `Mapped` / `mapped_column` style)
- SQLite (MVP)
- Pydantic v2 (schemas)
- Pytest
- Ruff (linting/formatting)

## Project Structure


## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Seed the database

```bash
python -m backend.seed.seed_data
```

This creates `chakravyuh.db` with fictional demo cases, including a
wallet shared across two active cases, a wallet matching a past closed
case, and a wallet flagged as a known mixer — so correlation logic can
be demonstrated end-to-end.

## Run tests

```bash
pytest
```

## Run the API (optional, for local testing)

```bash
uvicorn backend.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API docs.

## Correlation Logic

`backend/services/correlation.py` exposes:

- `correlate_wallet(db, wallet_address, exclude_case_id=None)` — checks
  a single wallet against active cases, past cases, and known entities.
- `correlate_case(db, case_id)` — runs correlation for every wallet in
  a case's trail.

## Out of Scope (handled by other members)

- Frontend
- Authentication
- Blockchain API integration / live wallet tracing
- ML-based risk scoring
- Report generation