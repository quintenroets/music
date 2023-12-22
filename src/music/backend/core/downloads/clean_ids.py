"""
Spotify changes the ids of its tracks sometimes run this file to give the downloaded
songs their most recent id.
"""

from typing import TypeVar

from ..client import spotapi
from ..utils import Path

T = TypeVar("T")
U = TypeVar("U")


def reverse(items: dict[T, U]) -> dict[U, T]:
    return {v: k for k, v in items.items()}


def main() -> None:
    downloads = Path.download_ids.yaml
    ids = list(downloads.keys())
    songs = spotapi.songs(ids)

    new_downloads = {song.id: title for song, title in zip(songs, downloads.values())}
    new_downloads = reverse(reverse(new_downloads))  # filter out duplicate song titles
    Path.download_ids.yaml = new_downloads


if __name__ == "__main__":
    main()
