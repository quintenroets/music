import cli

from ..client.response_types import Track
from ..utils import Path


def add(songs: list[Track]) -> None:
    if songs:
        songs = sorted(songs, key=lambda song: song.popularity, reverse=True)
        songs_mapper = {
            song.id: full_name(song) for song in songs if song.should_download
        }

        ids = Path.download_ids.yaml
        names = {v for v in ids.values()}
        # filter based on id or name because there can be two identical songs with a
        # different name (caused by different artist) or id (caused by different album)
        new_songs = {
            k: v for k, v in songs_mapper.items() if k not in ids and v not in names
        }

        for name in new_songs.values():
            cli.console.print(name)

        Path.to_download.update(new_songs)


def is_downloaded(song: Track) -> bool:
    ids = Path.download_ids.yaml
    names = {v for v in ids.values()}
    return song.id in ids or full_name(song) in names


def full_name(song: Track) -> str:
    artist_names = ", ".join([artist.name for artist in song.artists])
    name = f"{artist_names} - {song.name}"
    return name


def get() -> list[str]:
    return list(Path.to_download.yaml.keys())


def remove(song_ids: list[str]) -> None:
    to_download = Path.to_download.yaml
    songs_dict = {s: to_download[s] for s in song_ids}
    Path.download_ids.update(songs_dict)
    Path.to_download.yaml = {
        k: v for k, v in Path.to_download.yaml.items() if k not in song_ids
    }
