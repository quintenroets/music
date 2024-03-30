import cli

from ..context import context
from ..utils.progress import track_progress
from .artist import ArtistUpdater


def check_for_new_songs() -> None:
    description = "Checking for new songs"
    cli.console.clear_live()
    artists = track_progress(
        context.storage.artists, description=description, unit="artists"
    )
    for artist in artists:
        ArtistUpdater(artist).check_for_new_songs()
