import sys

import cli

from music.runtime import runtime
from music.utils.progress import track_progress

from .artist import ArtistUpdater


def check_for_new_songs() -> None:
    description = "Checking for new songs"
    cli.console.clear_live()
    if runtime.is_running_in_ci:
        check_for_new_songs_with_print_progress(description)  # pragma: nocover
    else:
        check_for_new_songs_with_rich_progress(description)


def check_for_new_songs_with_print_progress(
    description: str,
) -> None:  # pragma: nocover
    cli.console.print(description)
    number_of_artists = len(runtime.storage.artists)
    for i, artist in enumerate(runtime.storage.artists):
        cli.console.print(f"Checking {artist.name} ({i + 1}/{number_of_artists})")
        sys.stdout.flush()
        ArtistUpdater(artist).check_for_new_songs()


def check_for_new_songs_with_rich_progress(description: str) -> None:
    artists = track_progress(
        runtime.storage.artists,
        description=description,
        unit="artists",
    )
    for artist in artists:
        ArtistUpdater(artist).check_for_new_songs()
