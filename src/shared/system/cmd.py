import argparse
from config import settings


def domain_arg():
    """Define dominio como argumento de execução"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--domain",
        type=str,
        required=True,
    )

    return parser.parse_args()


def run_flow(flow_factory: callable):
    """Executa o flow dedicado para um domínio"""
    args = domain_arg()

    domain = args.domain
    database = settings.domain_db_path(domain=domain)

    flow_factory(database=database, domain=domain)
