from music.utils import Path, iteration

from . import downloader, jobs, postprocessor, uploader


def download():
    songs = jobs.get()
    if songs:
        for chunk in iteration.chunked(songs, chunk_size=20):
            _download(chunk)
    if not Path.processed_songs.is_empty():
        uploader.start()


def _download(songs):
    downloader.download(songs)
    postprocessor.process_downloads()
    jobs.remove(songs)
