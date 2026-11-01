import os
from pathlib import Path

from dotenv import load_dotenv

# carrega as variaveis do arquivo .env da raiz do projeto
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DB_URI = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ.get('DB_HOST', 'localhost')}:{os.environ.get('DB_PORT', '5432')}"
    f"/{os.environ['DB_NAME']}"
)
