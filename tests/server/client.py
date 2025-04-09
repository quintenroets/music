import json
import typing
from collections.abc import Mapping
from typing import Any

from fastapi.testclient import TestClient

from music.server import app


class RouteTestClient:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.client = TestClient(app)

    def get_response(
        self,
        url: str,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        full_url = self.name + "/" + url
        response = self.client.get(full_url, params=params)
        try:
            response_content = response.json()
        except json.JSONDecodeError:  # pragma: nocover
            raise ValueError(response.text) from None
        else:
            return typing.cast("dict[str, str]", response_content)
