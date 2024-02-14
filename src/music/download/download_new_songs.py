from ..context import context
from ..utils.batched import batched
from . import spotdl
from .downloader import Downloader


def download_new_songs() -> None:
    fix_song_count()
    size = context.config.download_chunk_size
    ids_to_download = context.storage.ids_to_download
    for ids in batched(ids_to_download, size=size):
        Downloader(ids).start()


def fix_song_count() -> None:
    num_songs = len(context.storage.tracks_to_download)
    progress_handler = spotdl.downloader.progress_handler
    progress_handler.set_song_count(num_songs)
    progress_handler.set_song_count = lambda count: None
