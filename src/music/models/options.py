from dataclasses import dataclass
from typing import Annotated

import typer

from .path import Path

clean_download_ids_help = (
    "Spotify changes the ids of its tracks from time to time.\n"
    "This command saves the most recent id of all downloaded tracks"
)

clean_download_ids_option = typer.Option(help=clean_download_ids_help)


@dataclass
class Options:
    config_path: Path = Path.config
    upload_to_phone: bool = True
    add: Annotated[str | None, typer.Option(help="song to add")] = None
    clean_download_ids: Annotated[bool, clean_download_ids_option] = False
    fix_mtimes_on_phone: bool = False
