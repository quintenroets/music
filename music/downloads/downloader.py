from spotdl.console import download as spotdl_downloader

from ..client import spotdl
from ..utils import Path

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
        download_songs(songs)
        songs = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))
        retries -= 1

    if songs and retries == 0:
        raise Exception("Max download retries reached")


def download_songs(songs):
    spotdl_downloader.download(songs, spotdl.downloader)
