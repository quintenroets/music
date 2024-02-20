import cli

from ..context import context
from .artist import ArtistUpdater


def check_for_new_songs() -> None:
    description = "Checking for new songs"
    cli.console.clear_live()
    artists = cli.progress(  # type: ignore
        context.storage.artists, description=description, unit="artists", cleanup=True
    )
    for artist in artists:
        ArtistUpdater(artist).check_for_new_songs()
