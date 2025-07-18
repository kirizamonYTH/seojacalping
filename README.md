curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv --version

git clone https://github.com/kirizamonYTH/scalpng-solana

uv venv
source .venv/bin/activate 

nano wallet.env (ubah private key)

uv run scalper.py
