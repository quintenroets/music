import typing
from typing import Any

from fastapi.testclient import TestClient
from music.server import app


class RouteTestClient:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.client = TestClient(app)

    def get_response(self, url: str, params: dict[str, str] | None = None) -> Any:
        full_url = self.name + "/" + url
        response = self.client.get(full_url, params=params).json()
        return typing.cast(dict[str, str], response)
