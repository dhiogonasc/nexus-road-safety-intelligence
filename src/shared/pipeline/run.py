from config import settings
from src.shared.system.cmd import domain_arg


def run_flow(flow_factory: callable):
    """Executa o flow dedicado para um domínio"""
    args = domain_arg()

    domain = args.domain
    database = settings.domain_db_path(domain=domain)

    flow_factory(database=database, domain=domain)