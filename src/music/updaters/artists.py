import sys
from typing import Iterator

import cli

from music.runtime import runtime
from music.utils.progress import track_progress

from .artist import ArtistUpdater
from music.models.artist import ArtistType, Artist


def check_for_new_songs() -> None:
    description = "Checking for new songs"
    cli.console.clear_live()
    for artist in generate_artists(description):
        ArtistUpdater(artist).check_for_new_songs()


def generate_artists(description: str) -> Iterator[Artist]:  # pragma: nocover
    if runtime.is_running_in_ci:
        cli.console.print(description)
        number_of_artists = len(runtime.storage.artists)
        for i, artist in enumerate(runtime.storage.artists):
            cli.console.print(f"Checking {artist.name} ({i + 1}/{number_of_artists})")
            sys.stdout.flush()
            yield artist
    else:
        yield from track_progress(
            runtime.storage.artists, description=description, unit="artists"
        )
