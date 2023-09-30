from dataclasses import dataclass

import cli
from spotdl.console import download as spotdl_downloader
from spotdl.download.downloader import Downloader as SpotifyDownloader

from ..client import get_spotdl_client
from ..utils import Path, iteration
from . import jobs, postprocessor

DOWNLOAD_RETRIES = 5


def clear_downloads():
    # existing downloads raise errors and can be removed because
    # successfully downloaded songs have already been moved to other folder
    Path.downloaded_songs.rmtree(remove_root=False)


@dataclass
class Downloader:
    songs: list[str]
    downloader: SpotifyDownloader = None
    chunk_size: int = 20

    def __post_init__(self):
        self.downloader = get_spotdl_client().downloader
        self.fix_song_count()

    def fix_song_count(self):
        num_songs = len(self.songs)
        self.downloader.progress_handler.set_song_count(num_songs)
        self.downloader.progress_handler.set_song_count = lambda count: None

    def start(self):
        for chunk in iteration.chunked(self.songs, chunk_size=self.chunk_size):
            self.download_songs_chunk(chunk)

    def download_songs_chunk(self, songs):
        self.download_songs(songs)
        with cli.status("Processing downloads"):
            postprocessor.process_downloads()
        jobs.remove(songs)

    def download_songs(self, songs):
        songs = [
            id_ if id_.startswith("http") else f"https://open.spotify.com/track/{id_}"
            for id_ in songs
        ]

        clear_downloads()
        tries_left = DOWNLOAD_RETRIES
        while songs and tries_left:
            spotdl_downloader.download(songs, self.downloader)
            songs = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))
            tries_left -= 1

        if songs and not tries_left:
            raise Exception("Max download retries reached")
