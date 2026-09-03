"""
CHAKRAVYUH - Member 3
Blockchain Fund Tracer

Responsibilities:
- Normalize wallet addresses
- Find outgoing transactions
- Trace funds for a maximum of 3 hops
- Prevent infinite loops
- Produce frontend-friendly transaction trail
"""

from typing import List, Dict, Any
from datetime import datetime


def normalize_address(address: str) -> str:
    """
    Normalize a blockchain address for comparison.

    Example:
        0xABCDEF -> 0xabcdef
    """

    if not isinstance(address, str):
        raise ValueError("Wallet address must be a string")

    return address.strip().lower()


def parse_timestamp(timestamp: str) -> datetime:
    """
    Convert ISO timestamp into datetime.

    Supported example:
        2026-08-28T10:00:00
        2026-08-28T10:00:00Z
    """

    if not isinstance(timestamp, str):
        raise ValueError("Timestamp must be a string")

    return datetime.fromisoformat(
        timestamp.replace("Z", "+00:00")
    )


def validate_transaction(tx: Dict[str, Any]) -> None:
    """
    Make sure a transaction contains the fields
    required by Member 3.
    """

    required_fields = [
        "tx_hash",
        "from_address",
        "to_address",
        "amount",
        "timestamp"
    ]

    for field in required_fields:
        if field not in tx:
            raise ValueError(
                f"Transaction missing required field: {field}"
            )


def get_outgoing_transactions(
    wallet_address: str,
    transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Return transactions sent FROM the specified wallet.

    Results are sorted chronologically.
    """

    wallet_address = normalize_address(wallet_address)

    outgoing = []

    for tx in transactions:

        validate_transaction(tx)

        sender = normalize_address(
            tx["from_address"]
        )

        if sender == wallet_address:
            outgoing.append(tx)

    outgoing.sort(
        key=lambda tx: parse_timestamp(
            tx["timestamp"]
        )
    )

    return outgoing


def trace_three_hops(
    start_wallet: str,
    transactions: List[Dict[str, Any]],
    max_hops: int = 3
) -> List[Dict[str, Any]]:
    """
    Trace fund movement starting from a suspect wallet.

    Maximum default depth = 3 hops.

    Example:

        A -> B -> C -> D

        A -> B = Hop 1
        B -> C = Hop 2
        C -> D = Hop 3
    """

    if max_hops < 1:
        raise ValueError("max_hops must be at least 1")

    start_wallet = normalize_address(start_wallet)

    # Validate all transactions before tracing
    for tx in transactions:
        validate_transaction(tx)

    results = []

    # Each item:
    # (wallet, hop_number, time_funds_reached_wallet, path_wallets)
    queue = [
        (
            start_wallet,
            1,
            None,
            {start_wallet}
        )
    ]

    while queue:

        current_wallet, hop, received_time, visited = queue.pop(0)

        if hop > max_hops:
            continue

        outgoing = get_outgoing_transactions(
            current_wallet,
            transactions
        )

        for tx in outgoing:

            tx_time = parse_timestamp(
                tx["timestamp"]
            )

            # If this wallet was reached by a previous
            # transaction, don't trace transactions that
            # happened before the funds arrived.
            if (
                received_time is not None
                and tx_time < received_time
            ):
                continue

            destination = normalize_address(
                tx["to_address"]
            )

            traced_tx = {
                "hop": hop,
                "tx_hash": tx["tx_hash"],
                "from_address": normalize_address(
                    tx["from_address"]
                ),
                "to_address": destination,
                "amount": float(tx["amount"]),
                "timestamp": tx["timestamp"]
            }

            results.append(traced_tx)

            # Continue to next hop
            if (
                hop < max_hops
                and destination not in visited
            ):

                next_visited = set(visited)
                next_visited.add(destination)

                queue.append(
                    (
                        destination,
                        hop + 1,
                        tx_time,
                        next_visited
                    )
                )

    # Sort final trail by hop and timestamp
    results.sort(
        key=lambda tx: (
            tx["hop"],
            parse_timestamp(tx["timestamp"])
        )
    )

    return results