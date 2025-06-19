from music import updaters


def test_clean_download_ids() -> None:
    updaters.download_ids.clean_download_ids()


def test_check_missing_downloads() -> None:
    updaters.download_ids.check_missing_downloads()
