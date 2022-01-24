from music.client.client import combine_chunks
from music.path import Path

from . import downloader, jobs, postprocessor, uploader


def download():
    songs = jobs.get()
    if songs:
        _download(songs)
    if not Path.processed_songs.is_empty():
        uploader.start()


@combine_chunks
def _download(songs):
    downloader.download(songs)
    postprocessor.process_downloads()
    jobs.remove(songs)
