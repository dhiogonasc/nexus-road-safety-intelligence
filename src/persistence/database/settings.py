from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from constants import ROOT


@dataclass
class DuckDBSettings:
    """ConfiguraÇção DuckDB"""

    DIRECTORY: str = Path(ROOT, "db").as_posix()
    EXTENSIONS: List[str] = field(
        default_factory=lambda: [
            "postgres",
            "httpfs",
            "parquet",
        ]
    )

    def database(self, catalog: str) -> str:
        """Chave de conexão"""
        return str(Path(self.DIRECTORY) / f"{catalog}.db")
