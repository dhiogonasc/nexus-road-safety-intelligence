from pathlib import Path

from constants import OCORRENCIAS_DIR

TABLES = [
    {
        "table_name": "raw_ocorrencias",
        "source_data_path": Path(OCORRENCIAS_DIR, "*.csv").as_posix(),
    }
]
