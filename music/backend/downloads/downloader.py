from spotdl.console import download as spotdl_downloader
from spotdl.download.downloader import Downloader as SpotifyDownloader

from ..client import get_spotdl_client
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
    tries_left = DOWNLOAD_RETRIES
    while songs and tries_left:
        Downloader.download_songs(songs)
        songs = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))
        tries_left -= 1

    if songs and not tries_left:
        raise Exception("Max download retries reached")


class Downloader:
    downloader: SpotifyDownloader = None

    @classmethod
    def download_songs(cls, songs):
        if cls.downloader is None:
            cls.downloader = get_spotdl_client().downloader
        else:
            cls.downloader.progress_handler.song_count += len(songs)
        spotdl_downloader.download(songs, cls.downloader)
