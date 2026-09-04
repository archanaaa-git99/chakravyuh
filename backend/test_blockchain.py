from backend.services.blockchain_service import get_wallet_transactions


wallet = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

transactions = get_wallet_transactions(
    wallet,
    page=2,
    offset=100
)

print("Number of transactions:", len(transactions))

if transactions:
    print("\nFirst transaction on page 2:")
    print(transactions[0])