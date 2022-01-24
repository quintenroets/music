"""
spotify changes the ids of its tracks sometimes
run this file to give the downloaded songs their most recent id
"""
from music.client import spotapi
from music.path import Path


def main():
    downloads = Path.download_ids.content
    ids = list(downloads.keys())
    songs = spotapi.songs(ids)

    new_downloads = {song.id: title for song, title in zip(songs, downloads.values())}
    Path.download_ids.content = new_downloads


if __name__ == "__main__":
    main()
