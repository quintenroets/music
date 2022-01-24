from typing import List, Union

import cli
from music.client.response_types import Track
from music.path import Path


def download_wanted(song: Track):
    skip_names = ("Interlude", "Intro", "Outro", "Live", "Instrumental")
    return (
        2 * 60 * 1000 < song.duration_ms < 10 * 60 * 1000
        and song.popularity > 15
        and not any([f" - {skip_name}" in song.name for skip_name in skip_names])
    )


def add(songs: List[Union[Track, str]], urls=False):
    if songs:
        if urls:
            songs = {song: "" for song in songs}
        else:
            songs = sorted(songs, key=lambda song: song.popularity, reverse=True)
            songs = {
                song.id: full_name(song) for song in songs if download_wanted(song)
            }

        ids = Path.download_ids.content
        names = {v for v in ids.values()}
        # filter based on equal id or name because there can be two identical songs with a different
        # name (caused by different artist) or id (caused by different album)
        new_songs = {k: v for k, v in songs.items() if k not in ids and v not in names}

        for name in new_songs.values():
            cli.console.print(name)

        Path.to_download.content |= new_songs


def full_name(song: Track):
    artist_names = ", ".join([artist.name for artist in song.artists])
    name = f"{artist_names} - {song.name}"
    return name


def get():
    return list(Path.to_download.content.keys())


def remove(song_ids: List[str]):
    to_download = Path.to_download.content
    Path.download_ids.content |= {s: to_download[s] for s in song_ids}
    Path.to_download.content = {
        k: v for k, v in Path.to_download.content.items() if k not in song_ids
    }
