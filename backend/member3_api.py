"""
CHAKRAVYUH - Member 3 API

Provides an API endpoint that accepts:
- suspect wallet address
- normalized blockchain transactions
- known risky addresses

and returns:
- 3-hop transaction trail
- first suspicious transition
- investigation result
"""

from typing import List, Dict, Any, Set

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.services.tracer import trace_three_hops

from backend.services.rule_engine import (
    find_first_suspicious_transition
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CHAKRAVYUH - Member 3 Intelligence API",
    description=(
        "Blockchain tracing and suspicious "
        "transaction analysis"
    ),
    version="1.0.0"
)


# =========================================================
# DATA MODELS
# =========================================================

class Transaction(BaseModel):

    tx_hash: str

    from_address: str

    to_address: str

    amount: float

    timestamp: str


class TraceRequest(BaseModel):

    wallet_address: str

    transactions: List[Transaction]

    risky_addresses: List[str] = []


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def home():

    return {
        "service": "CHAKRAVYUH Member 3",
        "status": "running",
        "module": "Blockchain Tracing + Rule Engine"
    }


# =========================================================
# TRACE ENDPOINT
# =========================================================

@app.post("/trace")
def trace_wallet(request: TraceRequest):

    try:

        # Convert Pydantic models into dictionaries
        transactions = [
            tx.model_dump()
            for tx in request.transactions
        ]

        # Convert risky address list into set
        risky_addresses: Set[str] = set(
            request.risky_addresses
        )

        # -------------------------------------------------
        # STEP 1 - TRACE
        # -------------------------------------------------

        trail = trace_three_hops(
            start_wallet=request.wallet_address,
            transactions=transactions,
            max_hops=3
        )

        # -------------------------------------------------
        # STEP 2 - INTELLIGENCE ANALYSIS
        # -------------------------------------------------

        suspicious_transition = (
            find_first_suspicious_transition(
                trail=trail,
                all_transactions=transactions,
                risky_addresses=risky_addresses
            )
        )

        # -------------------------------------------------
        # STEP 3 - RESPONSE
        # -------------------------------------------------

        return {

            "status": "success",

            "start_wallet": request.wallet_address,

            "trace": {
                "max_hops": 3,
                "transaction_count": len(trail),
                "transactions": trail
            },

            "first_suspicious_transition":
                suspicious_transition
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Internal tracing error: "
                + str(error)
            )
        )