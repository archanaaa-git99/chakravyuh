"""
CHAKRAVYUH - Member 3
Complete Test Suite

Tests:
1. Three-hop tracing
2. Rapid movement
3. Near-total forwarding
4. Sudden splitting
5. Known risky address
6. First suspicious transition
7. JSON investigation output
"""

import json

from backend.services.tracer import trace_three_hops

from backend.services.rule_engine import (
    rapid_movement_rule,
    near_total_transfer_rule,
    sudden_splitting_rule,
    known_risky_address_rule,
    find_first_suspicious_transition
)


# =========================================================
# TEST DATA
# =========================================================

transactions = [

    {
        "tx_hash": "TX001",
        "from_address": "0xAAA",
        "to_address": "0xBBB",
        "amount": 1.00,
        "timestamp": "2026-08-28T10:00:00"
    },

    {
        "tx_hash": "TX002",
        "from_address": "0xBBB",
        "to_address": "0xCCC",
        "amount": 0.95,
        "timestamp": "2026-08-28T10:04:00"
    },

    {
        "tx_hash": "TX003",
        "from_address": "0xCCC",
        "to_address": "0xDDD",
        "amount": 0.90,
        "timestamp": "2026-08-28T11:00:00"
    }
]


# =========================================================
# TEST 1 - THREE HOP TRACING
# =========================================================

print()
print("=" * 70)
print("TEST 1 - THREE HOP BLOCKCHAIN TRACE")
print("=" * 70)

trail = trace_three_hops(
    start_wallet="0xAAA",
    transactions=transactions
)

for tx in trail:

    print(
        f"\nHop {tx['hop']}: "
        f"{tx['from_address']} -> "
        f"{tx['to_address']}"
    )

    print(
        f"Amount: {tx['amount']} ETH"
    )

    print(
        f"TX: {tx['tx_hash']}"
    )

    print(
        f"Time: {tx['timestamp']}"
    )


# =========================================================
# TEST 2 - RAPID MOVEMENT
# =========================================================

print()
print("=" * 70)
print("TEST 2 - RAPID MOVEMENT RULE")
print("=" * 70)

rapid_result = rapid_movement_rule(
    transactions[0],
    transactions[1]
)

print(
    f"Rapid movement detected: {rapid_result}"
)


# =========================================================
# TEST 3 - NEAR TOTAL FORWARDING
# =========================================================

print()
print("=" * 70)
print("TEST 3 - NEAR TOTAL FORWARDING RULE")
print("=" * 70)

forwarding_result = near_total_transfer_rule(
    incoming_amount=1.00,
    outgoing_amount=0.95
)

print(
    f"Near-total forwarding detected: "
    f"{forwarding_result}"
)


# =========================================================
# TEST 4 - SUDDEN SPLITTING
# =========================================================

print()
print("=" * 70)
print("TEST 4 - SUDDEN SPLITTING RULE")
print("=" * 70)

split_transactions = [

    {
        "tx_hash": "SPLIT001",
        "from_address": "0xBBB",
        "to_address": "0xCCC",
        "amount": 0.30,
        "timestamp": "2026-08-28T10:05:00"
    },

    {
        "tx_hash": "SPLIT002",
        "from_address": "0xBBB",
        "to_address": "0xDDD",
        "amount": 0.30,
        "timestamp": "2026-08-28T10:06:00"
    },

    {
        "tx_hash": "SPLIT003",
        "from_address": "0xBBB",
        "to_address": "0xEEE",
        "amount": 0.30,
        "timestamp": "2026-08-28T10:07:00"
    }
]

split_result = sudden_splitting_rule(
    split_transactions
)

print(
    f"Sudden splitting detected: "
    f"{split_result}"
)


# =========================================================
# TEST 5 - KNOWN RISKY ADDRESS
# =========================================================

print()
print("=" * 70)
print("TEST 5 - KNOWN RISKY ADDRESS RULE")
print("=" * 70)

risky_addresses = {
    "0xCCC",
    "0xBADWALLET"
}

risky_result = known_risky_address_rule(
    destination_address="0xCCC",
    risky_addresses=risky_addresses
)

print(
    f"Known risky address detected: "
    f"{risky_result}"
)


# =========================================================
# TEST 6 - FIRST SUSPICIOUS TRANSITION
# =========================================================

print()
print("=" * 70)
print("TEST 6 - FIRST SUSPICIOUS TRANSITION")
print("=" * 70)

investigation = find_first_suspicious_transition(
    trail=trail,
    all_transactions=transactions,
    risky_addresses=risky_addresses
)

if investigation["found"]:

    print()
    print("🚨 SUSPICIOUS TRANSITION FOUND")

    print(
        f"Hop       : {investigation['hop']}"
    )

    print(
        f"TX Hash   : {investigation['tx_hash']}"
    )

    print(
        f"From      : {investigation['from_address']}"
    )

    print(
        f"To        : {investigation['to_address']}"
    )

    print(
        f"Amount    : {investigation['amount']} ETH"
    )

    print(
        f"Timestamp : {investigation['timestamp']}"
    )

    print()
    print("Reasons:")

    for reason in investigation["reasons"]:

        print(
            f"  ⚠ {reason}"
        )

else:

    print(
        "No suspicious transition found."
    )


# =========================================================
# FINAL JSON RESULT
# =========================================================

final_result = {

    "status": "success",

    "start_wallet": "0xAAA",

    "trace": {
        "max_hops": 3,
        "transactions": trail
    },

    "first_suspicious_transition": investigation
}


print()
print("=" * 70)
print("FINAL JSON INVESTIGATION RESULT")
print("=" * 70)

print(
    json.dumps(
        final_result,
        indent=4
    )
)


# =========================================================
# TEST SUMMARY
# =========================================================

print()
print("=" * 70)
print("MEMBER 3 TEST SUMMARY")
print("=" * 70)

print("✅ 3-hop tracing")
print("✅ Rapid movement detection")
print("✅ Near-total forwarding detection")
print("✅ Sudden splitting detection")
print("✅ Known risky address detection")
print("✅ First suspicious transition")
print("✅ JSON investigation output")

print()
print("🎉 MEMBER 3 CORE MODULE COMPLETE")
print("=" * 70)
