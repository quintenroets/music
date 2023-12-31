import argparse
from argparse import Namespace


def get_args() -> Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--no-phone", dest="no_phone", action="store_true", default=False
    )
    parser.add_argument("--add", default=None)
    args = parser.parse_args()
    return args


def get_backend_args() -> Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--headless", action="store_true", default=False)
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument(
        "--no-frontend-check",
        dest="no_frontend_check",
        action="store_true",
        default=False,
    )
    parser.add_argument("--backend", action="store_true", default=False)
    args = () if parser.prog == "pytest" else None
    return parser.parse_args(args)
