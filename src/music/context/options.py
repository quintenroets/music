from dataclasses import dataclass
from typing import Annotated

import typer

from music.models.path import Path


class Helps:
    clean_download_ids = (
        "Spotify changes the ids of its tracks from time to time.\n"
        "This command saves the most recent id of all downloaded tracks"
    )
    check_missing_downloads = (
        "Check downloaded ids to be actually present as downloaded "
        "songs and add missing ids to download queue"
    )


class TyperOptions:
    clean_download_ids = typer.Option(help=Helps.clean_download_ids)
    check_missing_downloads = typer.Option(help=Helps.check_missing_downloads)


@dataclass
class Options:
    config_path: Path = Path.config
    upload_to_phone: bool = True
    clean_download_ids: Annotated[bool, TyperOptions.clean_download_ids] = False
    check_missing_downloads: Annotated[bool, TyperOptions.check_missing_downloads] = (
        False
    )
    fix_mtimes_on_phone: bool = False
