import argparse
from config import settings


def run_flow(flow_factory: callable):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--schema",
        type=str,
        required=True,
        help="schema",
    )

    args = parser.parse_args()

    flow_factory(
        database=settings.DUCKDB_PATH,
        schema=args.schema,
    )
