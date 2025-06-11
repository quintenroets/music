from music import updaters
from music.models import Path
from music.runtime import runtime


def main() -> None:
    """
    Download new songs.
    """
    if runtime.ci_context is not None:  # pragma: nocover
        with runtime.ci_context:
            _main()
    else:
        _main()


def _main() -> None:
    if runtime.context.options.clean_download_ids:
        updaters.download_ids.clean_download_ids()
    else:
        collect_new_songs()


def collect_new_songs() -> None:
    upload_to_phone = should_upload_to_phone()
    if not upload_to_phone and not runtime.storage.tracks_ready_for_download:
        updaters.artists.check_for_new_songs()
    print(runtime.storage.tracks_to_download)
    if runtime.storage.tracks_ready_for_download:
        download_new_songs()
        upload_to_phone = should_upload_to_phone()
    if upload_to_phone:
        upload_new_downloads()


def should_upload_to_phone() -> bool:
    processed_songs_present = not Path.processed_songs.is_empty()
    return runtime.context.options.upload_to_phone and processed_songs_present


def download_new_songs() -> None:
    # lazy import for performance
    from music.download import download_new_songs

    download_new_songs.download_new_songs()


def upload_new_downloads() -> None:
    # lazy import for performance
    from . import uploader

    uploader.start()
