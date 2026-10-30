from .staging import routines as staging_routines
from .dimension import routines as dimension_routines
from .fact import routines as fact_routines

routines = staging_routines + dimension_routines + fact_routines
