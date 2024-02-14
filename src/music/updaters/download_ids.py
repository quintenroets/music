from collections.abc import Iterator

from ..context import context


def clean_download_ids() -> None:
    track_info_iterator = generate_tracks_with_unique_name()
    ids, names = zip(*track_info_iterator)
    tracks = context.spotify_client.songs(ids)
    downloaded_tracks = {track.id: name for track, name in zip(tracks, names)}
    context.storage.downloaded_tracks = downloaded_tracks


def generate_tracks_with_unique_name() -> Iterator[tuple[str, str]]:
    encountered_names = set()
    for id_, name in context.storage.downloaded_tracks.items():
        if name not in encountered_names:
            encountered_names.add(name)
            yield id_, name
