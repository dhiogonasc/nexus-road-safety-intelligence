from pipeline.stage.dag_bronze import flow_bronze
from pipeline.stage.dag_silver import flow_silver
from pipeline.stage.dag_gold import flow_gold

MEDALLION_FLOW = {
    "bronze": flow_bronze,
    "silver": flow_silver,
    "gold": flow_gold,
}
