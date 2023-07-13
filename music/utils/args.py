import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--no-phone", dest="no_phone", action="store_true", default=False
    )
    parser.add_argument("--add", default=None)
    args = parser.parse_args()
    return args
