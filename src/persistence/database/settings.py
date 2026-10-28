from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from constants import ROOT


@dataclass
class DuckDBSettings:
    """Configuração DuckDB"""

    DIRECTORY: str = Path(ROOT, "db").as_posix()

    def database(self, catalog: str) -> str:
        """Chave de conexão"""
        return str(Path(self.DIRECTORY) / f"{catalog}.db")
