"""
CHAKRAVYUH - Member 3
Suspicion Rule Engine

Rules:
1. Rapid movement
2. Near-total forwarding
3. Sudden splitting
4. Known risky destination

The engine returns the FIRST suspicious transition
and explains why it was flagged.
"""

from typing import List, Dict, Any, Set
from datetime import datetime


def parse_timestamp(timestamp: str) -> datetime:
    """
    Convert ISO timestamp to datetime.
    """

    return datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )


# =========================================================
# RULE 1 - RAPID MOVEMENT
# =========================================================

def rapid_movement_rule(
    previous_tx: Dict[str, Any],
    current_tx: Dict[str, Any],
    time_limit_minutes: int = 10
) -> bool:
    """
    Detect whether funds moved within a short period.

    Default:
        <= 10 minutes = suspicious
    """

    previous_time = parse_timestamp(
        previous_tx["timestamp"]
    )

    current_time = parse_timestamp(
        current_tx["timestamp"]
    )

    difference_minutes = (
        current_time - previous_time
    ).total_seconds() / 60

    return (
        0 <= difference_minutes <= time_limit_minutes
    )


# =========================================================
# RULE 2 - NEAR-TOTAL FORWARDING
# =========================================================

def near_total_transfer_rule(
    incoming_amount: float,
    outgoing_amount: float,
    threshold: float = 0.90
) -> bool:
    """
    Detect whether >=90% of received funds
    were forwarded.

    Example:

        Received = 1.00 ETH
        Sent     = 0.95 ETH

        Ratio = 95%

        Result = suspicious
    """

    if incoming_amount <= 0:
        return False

    ratio = outgoing_amount / incoming_amount

    return ratio >= threshold


# =========================================================
# RULE 3 - SUDDEN SPLITTING
# =========================================================

def sudden_splitting_rule(
    outgoing_transactions: List[Dict[str, Any]],
    minimum_destinations: int = 3
) -> bool:
    """
    Detect a wallet sending funds to at least
    3 different destination wallets.
    """

    destinations = set()

    for tx in outgoing_transactions:

        destination = (
            tx["to_address"]
            .strip()
            .lower()
        )

        destinations.add(destination)

    return len(destinations) >= minimum_destinations


# =========================================================
# RULE 4 - KNOWN RISKY ADDRESS
# =========================================================

def known_risky_address_rule(
    destination_address: str,
    risky_addresses: Set[str]
) -> bool:
    """
    Check whether a destination is present
    in the known risky address list.
    """

    destination = (
        destination_address
        .strip()
        .lower()
    )

    normalized_risky = {
        address.strip().lower()
        for address in risky_addresses
    }

    return destination in normalized_risky


# =========================================================
# MAIN INTELLIGENCE ENGINE
# =========================================================

def find_first_suspicious_transition(
    trail: List[Dict[str, Any]],
    all_transactions: List[Dict[str, Any]],
    risky_addresses: Set[str]
) -> Dict[str, Any]:
    """
    Analyze the traced trail and identify the FIRST
    suspicious transition.

    Returns a structured result suitable for:
    - API
    - frontend
    - graph visualization
    - investigation report
    """

    if not trail:

        return {
            "found": False,
            "reason": "No traced transactions found."
        }

    # Analyze chronologically
    ordered_trail = sorted(
        trail,
        key=lambda tx: parse_timestamp(
            tx["timestamp"]
        )
    )

    for index, tx in enumerate(ordered_trail):

        reasons = []

        # -------------------------------------------------
        # RULE 1 + RULE 2
        # -------------------------------------------------

        if index > 0:

            previous_tx = ordered_trail[index - 1]

            if rapid_movement_rule(
                previous_tx,
                tx
            ):

                reasons.append(
                    "Rapid movement of funds"
                )

            if near_total_transfer_rule(
                previous_tx["amount"],
                tx["amount"]
            ):

                reasons.append(
                    "Near-total forwarding of received funds"
                )

        # -------------------------------------------------
        # RULE 3
        # -------------------------------------------------

        outgoing_from_wallet = [
            transaction
            for transaction in all_transactions
            if (
                transaction["from_address"]
                .strip()
                .lower()
                ==
                tx["from_address"]
                .strip()
                .lower()
            )
        ]

        if sudden_splitting_rule(
            outgoing_from_wallet
        ):

            reasons.append(
                "Funds split across multiple destinations"
            )

        # -------------------------------------------------
        # RULE 4
        # -------------------------------------------------

        if known_risky_address_rule(
            tx["to_address"],
            risky_addresses
        ):

            reasons.append(
                "Destination is a known risky address"
            )

        # -------------------------------------------------
        # FIRST SUSPICIOUS TRANSITION
        # -------------------------------------------------

        if reasons:

            return {
                "found": True,
                "hop": tx["hop"],
                "tx_hash": tx["tx_hash"],
                "from_address": tx["from_address"],
                "to_address": tx["to_address"],
                "amount": tx["amount"],
                "timestamp": tx["timestamp"],
                "reasons": reasons
            }

    return {
        "found": False,
        "reason": "No suspicious transition detected."
    }