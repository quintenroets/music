import cli
import requests
from retry import retry

from music.client import spotapi
from music.utils import Path

from . import jobs

DOWNLOAD_RETRIES = 5


def clear_downloads():
    # existing downloads raise errors and can be removed because
    # successfully downloaded songs have already been moved to other folder
    Path.downloaded_songs.rmtree(remove_root=False)


def download(new_songs):
    songs = [
        id_ if "http" in id_ else f"https://open.spotify.com/track/{id_}"
        for id_ in new_songs
    ]

    clear_downloads()
    retries = DOWNLOAD_RETRIES
    while songs and retries > 0:
        start_download(songs)
        songs = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))
        retries -= 1

    if songs and retries == 0:
        raise Exception("Max download retries reached")


def start_download(songs):
    try:
        start_spotdl_download(songs)
    except Exception:  # noqa
        error_message = "Could not match any of the results on YouTube for"
        songs_without_match = [
            song
            for song in songs
            if error_message
            in start_spotdl_download((song,), capture_output=True).stdout
        ]
        if songs_without_match:
            names_without_match = [
                jobs.full_name(song) for song in spotapi.songs(songs_without_match)
            ]
            Path.fails.yaml = (Path.fails.yaml or []) + names_without_match
            songs = [s for s in songs if s not in songs_without_match]
            if songs:
                clear_downloads()
                start_spotdl_download(songs)
        else:
            raise


def start_spotdl_download(songs, capture_output=False):
    options = {
        "output-format": "opus",
        "output": Path.downloaded_songs,
        "download-threads": 10,
        "search-threads": 10,
    }
    return run("spotdl", options, songs, capture_output=capture_output)


@retry(requests.exceptions.ReadTimeout)
def run(*args, capture_output=False):
    try:
        return cli.run(*args, check=not capture_output, capture_output=capture_output)
    except requests.exceptions.ReadTimeout:
        cli.run("clear")
        raise
