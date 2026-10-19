"""src/shared/system/cmd.py"""

import argparse


def declare_arg(flag: str):
    """Declara argumento para prompt de comando"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        f"--{flag}",
        type=str,
        required=True,
    )

    return parser.parse_args()


def declare_domain():
    """Declara flag --domain para prompt de comando"""
    return declare_arg(flag="domain")
