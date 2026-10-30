from prefect import flow

from .dag_bronze import flow_bronze
from .dag_silver import flow_silver
from .dag_gold import flow_gold


@flow(
    name="Flow Main",
    flow_run_name="flow_main",
)
def flow_main():
    flow_bronze()
    flow_silver()
    flow_gold()


if __name__ == "__main__":
    flow_main()
