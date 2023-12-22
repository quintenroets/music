import typer

from dataclasses import dataclass


@dataclass
class Arguments:
    message: bool = False

    def __post_init__(self):
        print(self.message)


# from music.backend import main
def main(message: str = "hallo"):
    print(message)


def entry_point() -> None:
    # typer.run(main)
    arguments = typer.run(Arguments)
    print(arguments)
    main()


if __name__ == "__main__":
    entry_point()
