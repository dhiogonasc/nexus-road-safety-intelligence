from pathlib import Path

BASE_DIR = Path().resolve()

DATA_DIR = BASE_DIR / "data"

DATABASE_DIR = DATA_DIR / "db"

RAW_DIR = DATA_DIR / "raw"

ACIDENTES_DIR = RAW_DIR / "acidentes"
AC_OCORRENCIA_DIR = ACIDENTES_DIR / "ocorrencias"
AC_PESSOAS_DIR = ACIDENTES_DIR / "pessoas"

DUCKDB_INFO_DICT = {
    "extensions": [
        "postgres",
    ],
}