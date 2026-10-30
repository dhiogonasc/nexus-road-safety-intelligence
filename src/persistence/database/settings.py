from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from constants import DB_DIR


@dataclass
class DuckDBSettings:
    """Configuração DuckDB"""

    DIRECTORY: str = Path(DB_DIR).as_posix()

    def database(self, name: str, db_dir: Optional[str] = None) -> str:
        """Chave de conexão"""
        if db_dir:
            return Path(self.DIRECTORY, db_dir, f"{name}.db").as_posix()
        return Path(self.DIRECTORY, f"{name}.db").as_posix()

settings = DuckDBSettings()