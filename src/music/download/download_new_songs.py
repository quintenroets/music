import cli

from music.models import Path
from music.runtime import runtime
from music.utils.batched import batched

from . import spotdl
from .downloader import Downloader


def download_new_songs() -> None:
    print("DOWNLOAD")
    fix_song_count()
    size = runtime.context.config.download_chunk_size
    ids_to_download = runtime.storage.ids_to_download
    for ids in batched(ids_to_download, size=size):
        print(ids)
        Downloader(ids).start()
    download_youtube_songs()


def download_youtube_songs() -> None:
    urls = [
        f"https://www.youtube.com/watch?v={id_}"
        for id_ in runtime.storage.youtube_tracks_to_download
    ]
    if urls:
        options = {
            "output": str(Path.processed_songs / "%(title)s.%(ext)s"),
            "embed-thumbnail": None,
            "embed-metadata": None,
            "audio-format": "opus",
        }
        cli.run("yt-dlp", options, "-x", urls)
        runtime.storage.youtube_tracks_to_download = []


def fix_song_count() -> None:
    num_songs = len(runtime.storage.tracks_to_download)
    progress_handler = spotdl.downloader.progress_handler
    progress_handler.set_song_count(num_songs)
    progress_handler.set_song_count = lambda _: None
