from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from spotdl.utils.config import DOWNLOADER_OPTIONS

from ..utils import Path, tokens


def get_spotdl_client():
    options = get_download_options()
    return Spotdl(
        tokens.spotify.client_id,
        tokens.spotify.client_secret,
        downloader_settings=options,
    )


def get_download_options():
    output_path_format = str(Path.downloaded_songs / "{artists} - {title}.{output-ext}")
    DOWNLOADER_OPTIONS["format"] = "opus"
    DOWNLOADER_OPTIONS["output"] = output_path_format
    DOWNLOADER_OPTIONS["threads"] = 10
    return DownloaderOptions(**DOWNLOADER_OPTIONS)
