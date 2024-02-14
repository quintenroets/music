from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import cli
import pytest
from music.webapp.context import context
from music.webapp.context.context import Context
from music.webapp.main.main import Frontend, main


@pytest.fixture(scope="session")
def webapp_test_context() -> Iterator[Context]:
    context.config.backend_port += 7
    context.config.hostname = "https://music-test.com"
    context.config.session_name = "pytest-test-session"
    context.options.headless = True
    yield context


@pytest.fixture(scope="session")
def frontend_opening_context(webapp_test_context: Context) -> Iterator[Context]:
    webapp_test_context.options.headless = False
    yield webapp_test_context
    webapp_test_context.options.headless = True
    test_content_path = Frontend().content_path
    cli.run("sudo rm -r", test_content_path)


@patch("music.webapp.main.main.open_frontend")
def test_backend_start(_: MagicMock, webapp_test_context: Context) -> None:
    main()
    with pytest.raises(cli.exceptions.CalledProcessError):
        main()
    context.options.restart = True
    main()
    cli.run("tmux kill-session -t", webapp_test_context.config.session_name)


@patch("cli.urlopen")
@patch("music.webapp.main.main.start_backend")
def test_frontend_opening(
    open_url: MagicMock, _: MagicMock, frontend_opening_context: Context
) -> None:
    main()
    open_url.assert_called_once()
