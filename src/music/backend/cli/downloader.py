import typer

from music.core.main import main


def entry_point() -> None:
    typer.run(main)


if __name__ == "__main__":
    entry_point()
