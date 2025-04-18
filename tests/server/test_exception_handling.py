import typing
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

from music.server import app

from .client import RouteTestClient

if TYPE_CHECKING:
    from fastapi.responses import PlainTextResponse  # pragma: nocover


@patch("powertrace.visualize_traceback")
def test_exception_handling(mocked_visualize_traceback: MagicMock) -> None:
    error_message = "Test error"

    @app.get("/exception_test")
    def exception_test() -> None:
        raise RuntimeError(error_message)

    client = RouteTestClient()
    untyped_response = client.client.get("exception_test")
    response = typing.cast("PlainTextResponse", untyped_response)
    assert response.status_code == 500
    assert response.text == error_message  # type: ignore[attr-defined]
    mocked_visualize_traceback.assert_called_once()
