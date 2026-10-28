"""constants.py"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent

DATA_DIR = ROOT / "data"
DATABASE_DIR = DATA_DIR / "db"
RAW_DIR = DATA_DIR / "raw"

ACIDENTES_DIR = RAW_DIR / "acidentes"
AC_OCORRENCIA_DIR = ACIDENTES_DIR / "ocorrencias"
AC_PESSOAS_DIR = ACIDENTES_DIR / "pessoas"
