import cli
import requests

from retry import retry
from music.path import Path


def download(new_songs):
    # existing downloads raise errors and can be removed because successfully downloaded songs are moved to other folder
    Path.downloaded_songs.rmtree(remove_root=False)

    options = {
        "output-format": "opus",
        "output": Path.downloaded_songs,
        "download-threads": 10,
        "search-threads": 10,
    }
    songs = [
        id_ if "http" in id_ else f"https://open.spotify.com/track/{id_}"
        for id_ in new_songs
    ]

    prev_songs = None
    while songs and prev_songs != songs:
        run("spotdl", options, songs)
        prev_songs = songs
        songs = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))

    if songs:
        # prevent removing songs from to download
        raise Exception("Failed to download all songs")


@retry(requests.exceptions.ReadTimeout)
def run(*args):
    try:
        cli.run(*args)
    except requests.exceptions.ReadTimeout:
        cli.run("clear")
        raise
