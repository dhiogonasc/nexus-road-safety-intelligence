from pathlib import Path


def load_dir_files(dir_path: str | Path) -> dict[str, str]:
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
    path = Path(current_file).resolve().parent / "sql"

    if not path.is_dir():
        raise NotADirectoryError(f"O caminho '{path}' não é um diretório válido.")

    return load_dir_files(dir_path=path)
