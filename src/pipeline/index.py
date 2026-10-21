"""src/pipeline/index.py"""

from constants import AC_OCORRENCIA_DIR

PIPELINE_CONFIG = {
    # schema
    "acidentes": {
        # stage
        "bronze": {
            "ocorrencias": str(AC_OCORRENCIA_DIR / "*.csv"),
        },
        "silver": {},
        "gold": {},
    }
}
