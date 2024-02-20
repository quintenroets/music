from music import updaters


def test_clean_download_ids(mocked_storage: None) -> None:
    updaters.download_ids.clean_download_ids()
