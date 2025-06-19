from collections.abc import Iterator

from music.models.path import Path
from music.runtime import runtime


def clean_download_ids() -> None:
    track_info_iterator = generate_tracks_with_unique_name()
    ids, names = zip(*track_info_iterator, strict=False)
    tracks = runtime.spotify_client.songs(ids)
    downloaded_tracks = {
        track.id: name for track, name in zip(tracks, names, strict=False)
    }
    runtime.storage.downloaded_tracks = downloaded_tracks


def generate_tracks_with_unique_name() -> Iterator[tuple[str, str]]:
    encountered_names = set()
    for id_, name in runtime.storage.downloaded_tracks.items():
        if name not in encountered_names:
            encountered_names.add(name)
            yield id_, name


def check_missing_downloads() -> None:
    directories = Path.all_songs, Path.deleted
    downloaded_names = {
        path.stem for directory in directories for path in directory.iterdir()
    }
    runtime.storage.tracks_to_download = {
        id_: name
        for id_, name in runtime.storage.downloaded_tracks.items()
        if name.replace("?", "") not in downloaded_names
    }
