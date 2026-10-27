from typing import Dict, Callable

from ....staging.operation.registry import stage

operations: Dict[str, Callable] = {stage.__name__: stage}
