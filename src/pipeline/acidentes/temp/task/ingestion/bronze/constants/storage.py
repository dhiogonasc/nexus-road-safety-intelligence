from pathlib import Path

LAYER_PATH = Path(
    "acidentes",
    "bronze",
    "raw",
).as_posix()

STORAGE_PATH = Path(
    LAYER_PATH,
    "ocorrencia",
).as_posix()

LOG_PATH = Path(
    LAYER_PATH,
    "log",
    "ocorrencias",
).as_posix()
