import os
import time
import base58
import requests
from dotenv import load_dotenv
from solana.keypair import Keypair
from solana.rpc.api import Client

load_dotenv()

private_key = base58.b58decode(os.getenv("PRIVATE_KEY"))
keypair = Keypair.from_secret_key(private_key)
public_key = keypair.public_key
client = Client("https://api.mainnet-beta.solana.com")

TARGET_TOKEN = os.getenv("TARGET_TOKEN")
BUY_THRESHOLD = float(os.getenv("BUY_THRESHOLD", 0.95))
SELL_THRESHOLD = float(os.getenv("SELL_THRESHOLD", 1.10))
AMOUNT_SOL = float(os.getenv("AMOUNT_SOL", 0.01))
SOL_MINT = "So11111111111111111111111111111111111111112"

def get_quote(input_mint, output_mint, amount):
    url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippage=1"
    return requests.get(url).json()

def get_price():
    quote = get_quote(SOL_MINT, TARGET_TOKEN, int(AMOUNT_SOL * 1e9))
    if "data" in quote and len(quote["data"]) > 0:
        return float(quote["data"][0]["outAmount"]) / 1e6  # asumsikan token 6 desimal
    return None

def main():
    print("[INFO] Bot scalping dimulai...")
    base_price = get_price()
    if base_price is None:
        print("[ERR] Tidak bisa ambil harga awal.")
        return

    print(f"[INFO] Harga dasar: {base_price:.6f}")
    while True:
        try:
            current_price = get_price()
            if current_price is None:
                print("[WARN] Gagal ambil harga.")
                continue

            print(f"[INFO] Harga saat ini: {current_price:.6f}")
            if current_price <= base_price * BUY_THRESHOLD:
                print("[BUY] Harga turun. Siap beli (simulasi).")
                # TODO: tambahkan real swap
                base_price = current_price
            elif current_price >= base_price * SELL_THRESHOLD:
                print("[SELL] Harga naik. Siap jual (simulasi).")
                # TODO: tambahkan real swap
                base_price = current_price
        except Exception as e:
            print(f"[ERROR] {e}")

        time.sleep(5)

if __name__ == "__main__":
    main()
