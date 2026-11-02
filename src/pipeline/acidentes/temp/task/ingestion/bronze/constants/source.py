from pathlib import Path

from constants import AC_OCORRENCIAS_DIR

OCORRENCIA_SOURCE_PATH = Path(
    AC_OCORRENCIAS_DIR,
    "*.csv",
).as_posix()

SOURCE_PATHS = {
    "raw_ocorrencia": OCORRENCIA_SOURCE_PATH,
}
