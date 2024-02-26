from unittest.mock import MagicMock, patch

from music.cli import entry_point, webapp
from package_dev_utils.tests.args import no_cli_args


@no_cli_args
@patch("music.main._main.collect_new_songs")
def test_entry_point(_: MagicMock) -> None:
    entry_point.entry_point()


@no_cli_args
@patch("cli.run_commands")
@patch("cli.urlopen")
def test_webapp_entry_point(*_: MagicMock) -> None:
    webapp.entry_point()
