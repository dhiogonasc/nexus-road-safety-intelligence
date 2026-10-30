from .staging import routine as staging_routine
from .dimension import routines as dimension_routines
from .fact import routines as fact_routines

routines = [staging_routine] + dimension_routines + fact_routines
