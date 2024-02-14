import typing
from collections.abc import Iterator
from unittest.mock import PropertyMock, patch

import pytest
from music.models import Artist, Path
from music.storage import Storage


@pytest.fixture(scope="session")
def artist_info() -> list[dict[str, str]]:
    return [
        {"id": "4LLpKhyESsyAXpc4laK94U", "name": "Mac Miller", "type": "favorite"},
        {"id": "1VPmR4DJC1PlOtd0IADAO0", "name": "$uicideboy$", "type": "normal"},
        {
            "id": "2XnBwblw31dfGnspMIwgWz",
            "name": "Axwell /\\ Ingrosso",
            "type": "normal",
        },
        {"id": "6AgTAQt8XS6jRWi4sX7w49", "name": "Polo G", "type": "normal"},
    ]


def calculate_protected_folder_hash() -> str | None:
    return typing.cast(str, Path.assets.content_hash) if Path.assets.exists() else None


@pytest.fixture(scope="session")
def no_assets_modify() -> Iterator[None]:
    hash_value = calculate_protected_folder_hash()
    yield
    assert calculate_protected_folder_hash() == hash_value


@pytest.fixture(scope="session")
def artists(
    no_assets_modify: None, artist_info: list[dict[str, str]]
) -> Iterator[list[Artist]]:
    storage = Storage()
    with Path.tempfile() as path:
        path.yaml = typing.cast(dict[str, str], artist_info)
        mock_path = PropertyMock(return_value=path)
        with patch.object(Path, "artists", new_callable=mock_path):
            yield storage.artists


@pytest.fixture(scope="session")
def artist(artists: list[Artist]) -> Iterator[Artist]:
    yield artists[0]
