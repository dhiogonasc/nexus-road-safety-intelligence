from typing import Dict

from src.shared.model.pipeline import Catalog

from .acidentes import catalog as acidentes_catalog

catalogs: Dict[str, Catalog] = {acidentes_catalog.label: acidentes_catalog}
