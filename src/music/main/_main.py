from music import updaters
from music.context import context
from music.models import Path


def main() -> None:
    """
    Download new songs.
    """
    if context.ci_context is not None:  # pragma: nocover
        with context.ci_context:
            _main()
    else:
        _main()


def _main() -> None:
    if context.options.clean_download_ids:
        updaters.download_ids.clean_download_ids()
    else:
        if context.options.add is not None:
            tracks = [context.options.add]
            updaters.tracks.add_tracks_by_name(tracks)
        collect_new_songs()


def collect_new_songs() -> None:
    upload_to_phone = should_upload_to_phone()
    if not upload_to_phone and not context.storage.tracks_to_download:
        updaters.artists.check_for_new_songs()
    if context.storage.tracks_to_download:
        download_new_songs()
        upload_to_phone = should_upload_to_phone()
    if upload_to_phone:
        upload_new_downloads()


def should_upload_to_phone() -> bool:
    processed_songs_present = not Path.processed_songs.is_empty()
    return context.options.upload_to_phone and processed_songs_present


def download_new_songs() -> None:
    # lazy import for performance
    from music.download import download_new_songs

    download_new_songs.download_new_songs()


def upload_new_downloads() -> None:
    # lazy import for performance
    from . import uploader

    uploader.start()
