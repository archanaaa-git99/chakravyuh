import requests
from datetime import datetime, timezone
from backend.config import settings


ETHERSCAN_URL = "https://api.etherscan.io/v2/api"

def convert_timestamp(timestamp: str) -> str:
    return datetime.fromtimestamp(
        int(timestamp),
        tz=timezone.utc
    ).isoformat()

def validate_wallet_address(wallet_address: str) -> bool:
    if not wallet_address:
        return False

    if not wallet_address.startswith("0x"):
        return False

    if len(wallet_address) != 42:
        return False

    try:
        int(wallet_address[2:], 16)
    except ValueError:
        return False

    return True


def get_wallet_transactions(wallet_address: str,
                            page: int = 1,
                            offset: int = 100):
    if not validate_wallet_address(wallet_address):
        raise ValueError("Invalid Ethereum wallet address")

    params = {
        "chainid": "1",
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "page": page,
        "offset": offset,
        "sort": "asc",
        "apikey": settings.ETHERSCAN_API_KEY,
    }

    try:
        response = requests.get(
            ETHERSCAN_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise RuntimeError(
            f"Failed to connect to Etherscan: {error}"
        ) from error

    data = response.json()

    validate_etherscan_response(data)

    transactions = data.get("result", [])

    return [normalize_transaction(tx) for tx in transactions]

def normalize_transaction(transaction: dict) -> dict:
    return {
        "tx_hash": transaction["hash"],
        "from_address": transaction["from"],
        "to_address": transaction["to"],
        "amount": int(transaction["value"]) / 10**18,
        "timestamp": convert_timestamp(transaction["timeStamp"]),
    }
def validate_etherscan_response(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("Invalid response from Etherscan")

    if data.get("status") == "0":
        message = data.get("message", "Unknown Etherscan error")
        result = data.get("result", "")

        # Etherscan can use status=0 for "no transactions"
        if result == []:
            return

        raise RuntimeError(f"Etherscan API error: {message} - {result}")

    if data.get("status") != "1":
        raise RuntimeError("Unexpected response from Etherscan")


