"""src/shared/system/file.py"""

from importlib import resources
from pathlib import Path

from types import ModuleType
from typing import Dict, Union


def load_dir_files(dir_path: str | Path) -> dict[str, str]:
    """Carrega o conteudo dos arquivos de um diretorio em um dicionario"""
    path = Path(dir_path)
    files_dict = {}

    if not path.is_dir():
        raise NotADirectoryError(f"O caminho '{dir_path}' não é um diretório válido.")

    for file_path in path.iterdir():
        if file_path.is_file():
            try:
                files_dict[file_path.stem] = file_path.read_text(encoding="utf-8")
            except ValueError as e:
                print(f"Não foi possível ler o arquivo {file_path.name}: {e}")

    return files_dict


def load_module_queries(current_file: str | Path) -> dict[str, str]:
    """
    Carrega os scripts sql de um diretorio em um dicionario
    de acordo com a estrutura definida no projeto
    """
    path = Path(current_file).resolve().parent / "sql"

    if not path.is_dir():
        raise NotADirectoryError(f"O caminho '{path}' não é um diretório válido.")

    return load_dir_files(dir_path=path)


def load_module(module: Union[str, ModuleType]) -> Dict[str, str]:
    module_dict: Dict[str, str] = {}
    try:
        module_dict = {
            file_path.stem: file_path.read_text()
            for file_path in resources.files(module).iterdir()
            if file_path.is_file()
        }
    except Exception as e:
        pass

    return module_dict
