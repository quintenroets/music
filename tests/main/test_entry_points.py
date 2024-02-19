from unittest.mock import MagicMock, patch

from music.cli import entry_point
from music.webapp.cli.backend import entry_point as backend_entry_point
from music.webapp.cli.entry_point import entry_point as webapp_entry_point
from package_dev_utils.tests.args import no_cli_args


@no_cli_args
@patch("music.main.main.collect_new_songs")
def test_entry_point(_: MagicMock) -> None:
    entry_point()


@no_cli_args
@patch("cli.run_commands")
@patch("cli.urlopen")
def test_webapp_entry_point(*_: MagicMock) -> None:
    webapp_entry_point()


@no_cli_args
@patch("uvicorn.run")
def test_backend_entry_point(_: MagicMock) -> None:
    backend_entry_point()
