from __future__ import annotations

from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from spotdl.utils.config import DOWNLOADER_OPTIONS

from ..models import Path, Secrets


class Client(Spotdl):  # type: ignore
    @classmethod
    def create(cls, secrets: Secrets) -> Client:
        options = cls.create_downloader_options()
        return cls(
            secrets.spotify.client_id,
            secrets.spotify.client_secret,
            downloader_settings=options,
        )

    @classmethod
    def create_downloader_options(cls) -> DownloaderOptions:
        output_format = str(Path.downloaded_songs / "{artists} - {title}.{output-ext}")
        custom_options = {"output": output_format, "format": "opus", "threads": 10}
        options = DOWNLOADER_OPTIONS | custom_options
        return DownloaderOptions(**options)
