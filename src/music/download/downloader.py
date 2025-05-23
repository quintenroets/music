from dataclasses import dataclass

import cli
from spotdl.console.download import download

from music.models import Path
from music.runtime import runtime

from . import downloaded_songs_processor, spotdl


@dataclass
class Downloader:
    track_ids: list[str]

    def start(self) -> None:
        self.clear_downloads_path()
        self.download_songs()
        with cli.status("Processing downloads"):
            downloaded_songs_processor.run()
        self.update_downloaded_tracks()
        self.update_tracks_to_download()

    @classmethod
    def clear_downloads_path(cls) -> None:
        # existing downloads raise errors and can be removed because
        # successfully downloaded songs have already been moved to another folder
        for path in Path.downloaded_songs.iterdir():
            path.unlink()

    def create_download_urls(self) -> list[str]:
        return [
            id_ if id_.startswith("http") else f"https://open.spotify.com/track/{id_}"
            for id_ in self.track_ids
        ]

    def download_songs(self) -> None:
        tries_left = runtime.context.config.download_retries
        urls = self.create_download_urls()
        while urls and tries_left:
            download(urls, spotdl.downloader)
            urls = list(Path.downloaded_songs.glob("*.spotdlTrackingFile"))
            tries_left -= 1

        if urls and not tries_left:
            message = "Max download retries reached"
            raise RuntimeError(message)

    def update_downloaded_tracks(self) -> None:
        tracks_to_download = runtime.storage.tracks_to_download
        downloaded_tracks = {id_: tracks_to_download[id_] for id_ in self.track_ids}
        runtime.storage.downloaded_tracks |= downloaded_tracks

    def update_tracks_to_download(self) -> None:
        tracks_to_download = runtime.storage.tracks_to_download
        for id_ in self.track_ids:
            tracks_to_download.pop(id_)
        runtime.storage.tracks_to_download = tracks_to_download
