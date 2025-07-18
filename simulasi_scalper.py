import time
import requests

# Konfigurasi token
TARGET_TOKEN = "Es9vMFrzaCERqLkGgRbGzmiXbKQPY5vkjog49zjNHTy"  # ganti ke token target
SOL_MINT = "So11111111111111111111111111111111111111112"     # SOL token mint
AMOUNT_SOL = 0.01                                            # 0.01 SOL
BUY_THRESHOLD = 0.95
SELL_THRESHOLD = 1.10

def get_quote(input_mint, output_mint, amount):
    url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippage=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("[ERR] Gagal ambil data dari Jupiter")
        return None

def get_price():
    quote = get_quote(SOL_MINT, TARGET_TOKEN, int(AMOUNT_SOL * 1e9))
    if quote and "data" in quote and len(quote["data"]) > 0:
        out_amt = float(quote["data"][0]["outAmount"])
        return out_amt / 1e6  # asumsikan token target 6 desimal
    return None

def main():
    print("🚀 Bot simulasi scalping dimulai...")
    base_price = get_price()
    if base_price is None:
        print("[ERR] Gagal mendapatkan harga awal.")
        return

    print(f"[INFO] Harga awal (baseline): {base_price:.6f}")
    
    while True:
        current_price = get_price()
        if current_price is None:
            print("[WARN] Gagal mendapatkan harga.")
            time.sleep(5)
            continue

        print(f"[INFO] Harga sekarang: {current_price:.6f}")

        if current_price <= base_price * BUY_THRESHOLD:
            print(f"[BUY] Harga turun ke {current_price:.6f} -> beli!")
            base_price = current_price  # reset baseline setelah beli
        elif current_price >= base_price * SELL_THRESHOLD:
            print(f"[SELL] Harga naik ke {current_price:.6f} -> jual!")
            base_price = current_price  # reset baseline setelah jual

        time.sleep(5)

if __name__ == "__main__":
    main()
