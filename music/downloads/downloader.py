import cli
import requests
from retry import retry

from music.path import Path


def download(new_songs):
    # existing downloads raise errors and can be removed because
    # successfully downloaded songs have already been moved to other folder
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

    retries = 5

    while songs and retries > 0:
        run("spotdl", options, songs)
        songs = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))
        retries -= 1

    if songs and retries == 0:
        raise Exception("Max download retries reached")


@retry(requests.exceptions.ReadTimeout)
def run(*args):
    try:
        cli.run(*args)
    except requests.exceptions.ReadTimeout:
        cli.run("clear")
        raise
