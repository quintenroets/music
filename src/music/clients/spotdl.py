from __future__ import annotations

from typing import TYPE_CHECKING

from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from spotdl.utils.config import DOWNLOADER_OPTIONS

from music.models import Path

if TYPE_CHECKING:
    from music.context import Secrets  # pragma: nocover


class Client(Spotdl):  # type: ignore[misc]
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
        output_format = "{artists} - {title}.{output-ext}"
        custom_options = {
            "output": output_format,
            "format": "opus",
            "threads": 10,
            "print_errors": True,
            "log_level": "debug",
            "save_file": "out.json",
        }
        options = DOWNLOADER_OPTIONS | custom_options
        return DownloaderOptions(**options)
