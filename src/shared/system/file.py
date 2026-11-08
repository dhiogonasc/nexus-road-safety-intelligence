from importlib import resources
from types import ModuleType
from typing import Dict, Union


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
