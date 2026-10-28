"""constants.py"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DB_DIR = DATA_DIR / "db"

ACIDENTES_DIR = RAW_DIR / "acidentes"
AC_OCORRENCIAS_DIR = ACIDENTES_DIR / "ocorrencias"
