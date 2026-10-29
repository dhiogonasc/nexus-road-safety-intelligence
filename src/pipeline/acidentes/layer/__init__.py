from typing import List

from src.shared.model.pipeline import Layer

from .silver import layer as silver_layer
from .gold import layer as gold_layer

layers: List[Layer] = [silver_layer, gold_layer]