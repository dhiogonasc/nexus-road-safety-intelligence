from rpds import List

from src.shared.model.pipeline import Routine

from .ocorrencias import routine as ocorrencias_routine

routines: List[Routine] = [ocorrencias_routine]
