import pytest

from backend.services.blockchain_service import (
    validate_wallet_address,
    convert_timestamp,
    normalize_transaction,
)


def test_valid_wallet_address():
    wallet = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

    assert validate_wallet_address(wallet) is True


def test_invalid_wallet_address():
    wallet = "0x12345"

    assert validate_wallet_address(wallet) is False


def test_invalid_characters_in_wallet():
    wallet = "0xZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"

    assert validate_wallet_address(wallet) is False


def test_timestamp_conversion():
    result = convert_timestamp("1443428683")

    assert result == "2015-09-28T08:24:43+00:00"


def test_transaction_normalization():
    transaction = {
        "hash": "0xabc123",
        "from": "0x1111111111111111111111111111111111111111",
        "to": "0x2222222222222222222222222222222222222222",
        "value": "250000000000000000",
        "timeStamp": "1443428683",
    }

    result = normalize_transaction(transaction)

    assert result["tx_hash"] == "0xabc123"
    assert result["from_address"] == transaction["from"]
    assert result["to_address"] == transaction["to"]
    assert result["amount"] == 0.25
    assert result["timestamp"] == "2015-09-28T08:24:43+00:00"