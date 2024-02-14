from music.context import context

from .. import updaters
from ..models import Path
from . import uploader


def main() -> None:
    """
    Download new songs.
    """
    if context.options.clean_download_ids:
        updaters.download_ids.clean_download_ids()
    else:
        if context.options.add is not None:
            tracks = [context.options.add]
            updaters.tracks.add_tracks_by_name(tracks)
        collect_new_songs()


def collect_new_songs() -> None:
    processed_songs_present = not Path.processed_songs.is_empty()
    should_upload_to_phone = context.options.upload_to_phone and processed_songs_present
    should_check_updates = (
        not should_upload_to_phone and not context.storage.tracks_to_download
    )
    if should_check_updates:
        updaters.artists.check_for_new_songs()

    if context.storage.tracks_to_download:
        download_new_songs()

    if not Path.processed_songs.is_empty():
        uploader.start()


def download_new_songs() -> None:
    # lazy import for performance
    from .. import download

    download.download_new_songs()
