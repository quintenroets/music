from collections.abc import Iterator

import cli

from ..context import context
from ..models.response_types import Track


def add_tracks_by_name(names: list[str]) -> None:
    tracks_iterator = generate_new_tracks_by_name(names)
    tracks = list(tracks_iterator)
    if tracks:
        context.storage.save_new_tracks(tracks)


def generate_new_tracks_by_name(names: list[str]) -> Iterator[Track]:
    for name in names:
        tracks = context.spotify_client.search_song(name)
        yield from process_search_results(tracks)


def process_search_results(tracks: list[Track]) -> Iterator[Track]:
    show_results = True
    while show_results and tracks:
        track = tracks.pop(0)
        message = f"{track.full_name}\nDownload?"
        if cli.confirm(message):  # type: ignore
            yield track
            show_results = False
        else:
            show_results = cli.confirm("See next result?")  # type: ignore
