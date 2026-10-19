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
