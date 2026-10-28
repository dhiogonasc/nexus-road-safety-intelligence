from typing import List

from src.shared.model.pipeline import Layer

from .bronze import layer as bronze_layer
from .silver import layer as silver_layer

layers: List[Layer] = [bronze_layer, silver_layer]