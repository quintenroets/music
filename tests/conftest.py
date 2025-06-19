import typing
from collections.abc import Iterator
from unittest.mock import PropertyMock, patch

import cli
import pytest
import spotipy
from package_utils.storage import CachedFileContent

from music.clients import spotdl, spotify
from music.download.spotdl import downloader
from music.models import Artist, Path
from music.models.response_types import Track
from music.runtime import Runtime
from music.runtime import runtime as runtime_
from tests import mocks
from tests.mocks import Storage, mocked_method
from tests.mocks.client import mock_internal_call


@pytest.fixture(scope="session", autouse=True)
def _no_assets_modify() -> Iterator[None]:
    hash_value = calculate_protected_folder_hash()
    yield
    assert calculate_protected_folder_hash() == hash_value


def calculate_protected_folder_hash() -> str | None:
    return (
        typing.cast("str", Path.assets.content_hash) if Path.assets.exists() else None
    )


@pytest.fixture(scope="session")
def runtime() -> Runtime:
    return runtime_


@pytest.fixture(scope="session")
def _mocked_session_storage(runtime: Runtime) -> Iterator[None]:
    storage = Storage()
    mock_storage = PropertyMock(return_value=storage)
    patched_methods = [
        mocked_method(CachedFileContent, "__get__", mocks.CachedFileContent.__get__),
        mocked_method(CachedFileContent, "__set__", mocks.CachedFileContent.__set__),
    ]
    patched_storage = patch.object(runtime, "storage", new_callable=mock_storage)
    patched_cli_methods = [
        patch.object(cli.console, "print"),
        patch("cli.track_progress", new=lambda *args, **_: args[0]),
    ]
    patches = [patched_storage, *patched_methods, *patched_cli_methods]
    with patches[0], patches[1], patches[2], patches[3], patches[4]:
        yield


@pytest.fixture(autouse=True)
def _mocked_storage(_mocked_session_storage: None, runtime: Runtime) -> None:
    storage = typing.cast("Storage", runtime.storage)
    storage.reset()


@pytest.fixture(autouse=True, scope="session")
def _mocked_spotipy_client() -> Iterator[None]:
    patch_ = patch.object(spotipy.Spotify, "_internal_call", autospec=True)
    with patch_ as mocked_spotipy_client:
        mocked_spotipy_client.side_effect = mock_internal_call
        yield


@pytest.fixture(scope="session")
def artists(runtime: Runtime, _mocked_session_storage: None) -> list[Artist]:
    return runtime.storage.artists


@pytest.fixture(scope="session")
def artist(artists: list[Artist]) -> Artist:
    return artists[0]


@pytest.fixture(scope="session")
def client(runtime: Runtime) -> spotify.Client:
    return spotify.Client(runtime.context.secrets)


@pytest.fixture(scope="session")
def tracks(runtime: Runtime, artist: Artist) -> list[Track]:
    return runtime.spotify_client.top_songs(artist.id)[:2]


@pytest.fixture(scope="session")
def track(tracks: list[Track]) -> Track:
    return tracks[0]


@pytest.fixture
def _mocked_download_assets() -> Iterator[None]:
    path = Path.tempdir()
    mocked_path = PropertyMock(return_value=path)
    mock = patch.object(Path, "download_assets", new_callable=mocked_path)
    with mock, path:
        downloader.settings = spotdl.Client.create_downloader_options()
        yield
    downloader.settings = spotdl.Client.create_downloader_options()
