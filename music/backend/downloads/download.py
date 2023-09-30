from music.backend.utils import Path

from . import downloader, jobs, uploader


def download():
    songs = jobs.get()
    if songs:
        downloader.Downloader(songs).start()
    if not Path.processed_songs.is_empty():
        uploader.start()
