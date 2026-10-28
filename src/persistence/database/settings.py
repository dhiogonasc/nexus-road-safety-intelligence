from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from constants import DB_DIR


@dataclass
class DuckDBSettings:
    """Configuração DuckDB"""

    DIRECTORY: str = Path(DB_DIR).as_posix()

    def database(self, catalog: str) -> str:
        """Chave de conexão"""
        return Path(self.DIRECTORY, f"{catalog}", f"{catalog}.db").as_posix()
