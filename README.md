curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv --version

git clone https://github.com/kirizamonYTH/scalpng-solana

uv venv
source .venv/bin/activate 

uv pip install solana python-dotenv requests base58

nano wallet.env (ubah private key)

uv run scalper.py

jika gagal.. coba berikan perintah : 
uv pip uninstall solana
uv pip install solana==0.27.0

lalu jalnkan ulang dengan perintah : uv run scalper.py
