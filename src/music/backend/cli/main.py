import typer

from ..main.main import main as _main


def main() -> None:
    typer.run(_main)


if __name__ == "__main__":
    main()
