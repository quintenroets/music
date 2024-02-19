import typing
from collections.abc import Iterator
from unittest.mock import PropertyMock, patch

import cli
import pytest
from music.clients import spotdl, spotify
from music.context import Context
from music.context import context as context_
from music.context import context as global_context
from music.download.spotdl import downloader
from music.models import Artist, Path
from music.models.response_types import Track
from package_utils.storage import CachedFileContent

from tests import mocks
from tests.mocks import Storage, mocked_method


@pytest.fixture(scope="session")
def no_assets_modify() -> Iterator[None]:
    hash_value = calculate_protected_folder_hash()
    yield
    assert calculate_protected_folder_hash() == hash_value


def calculate_protected_folder_hash() -> str | None:
    return typing.cast(str, Path.assets.content_hash) if Path.assets.exists() else None


@pytest.fixture(scope="session")
def context(no_assets_modify: None) -> Context:
    return context_


@pytest.fixture(scope="session")
def _mocked_storage(context: Context) -> Iterator[None]:
    storage = Storage()
    mock_storage = PropertyMock(return_value=storage)
    patched_methods = [
        mocked_method(CachedFileContent, "__get__", mocks.CachedFileContent.__get__),
        mocked_method(CachedFileContent, "__set__", mocks.CachedFileContent.__set__),
    ]
    contexts = context, global_context
    patched_storages = [
        patch.object(context_, "storage", new_callable=mock_storage)
        for context_ in contexts
    ]
    patched_cli_methods = [
        patch.object(cli.console, "print"),
        patch("cli.progress", new=lambda *args, **kwargs: args[0]),
    ]
    patches = [*patched_storages, *patched_methods, *patched_cli_methods]
    with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5]:
        yield None


@pytest.fixture
def mocked_storage(_mocked_storage: None, context: Context) -> None:
    storage = typing.cast(Storage, context.storage)
    storage.reset()


@pytest.fixture(scope="session")
def artists(context: Context, _mocked_storage: None) -> list[Artist]:
    return context.storage.artists


@pytest.fixture(scope="session")
def artist(artists: list[Artist]) -> Artist:
    return artists[0]


@pytest.fixture(scope="session")
def client(context: Context) -> spotify.Client:
    return spotify.Client(context.secrets)


@pytest.fixture(scope="session")
def tracks(context: Context, artist: Artist) -> list[Track]:
    return context.spotify_client.top_songs(artist.id)


@pytest.fixture(scope="session")
def track(tracks: list[Track]) -> Track:
    return tracks[0]


@pytest.fixture
def mocked_download_assets() -> Iterator[None]:
    path = Path.tempfile(create=False)
    path.mkdir()
    mocked_path = PropertyMock(return_value=path)
    mock = patch.object(Path, "download_assets", new_callable=mocked_path)
    with mock, path:
        downloader.settings = spotdl.Client.create_downloader_options()
        yield
    downloader.settings = spotdl.Client.create_downloader_options()
