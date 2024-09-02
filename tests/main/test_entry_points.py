from unittest.mock import MagicMock, patch

from package_dev_utils.tests.args import no_cli_args

from music.cli import entry_point, webapp


@no_cli_args
@patch("music.main._main.collect_new_songs")
def test_entry_point(collect_new_songs: MagicMock) -> None:
    entry_point.entry_point()
    collect_new_songs.assert_called()


@no_cli_args
@patch("webapp_starter.main.main.start_backend")
@patch("webapp_starter.main.main.open_frontend")
def test_webapp_entry_point(start_backend: MagicMock, open_frontend: MagicMock) -> None:
    webapp.entry_point()
    for method in start_backend, open_frontend:
        method.assert_called_once()
