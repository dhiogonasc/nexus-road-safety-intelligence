"""constants.py"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DB_DIR = DATA_DIR / "db"

ACIDENTES_DIR = RAW_DIR / "acidentes"
SOURCE_OCORRENCIAS = Path(ACIDENTES_DIR, "ocorrencias", "*.csv").as_posix()
