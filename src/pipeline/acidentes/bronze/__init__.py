from shared.model.pipeline import SchemaRoutine

from .ocorrencias import routine as ocorrencias_routine

schema_routine = SchemaRoutine(routines=[ocorrencias_routine])
