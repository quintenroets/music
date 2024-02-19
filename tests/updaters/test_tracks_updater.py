from unittest.mock import MagicMock, patch

import pytest
from music import updaters
from music.context import Context
from music.models.response_types import Track


@pytest.fixture
def track_names(track: Track) -> list[str]:
    return [track.name]


@patch("cli.confirm", return_value=True)
def test_tracks_confirmed(
    _: MagicMock, context: Context, mocked_storage: None, track: Track
) -> None:
    names = [track.name]
    updaters.tracks.add_tracks_by_name(names)
    assert track.id in context.storage.tracks_to_download


@patch("cli.confirm", return_value=False)
def test_tracks_not_confirmed(
    _: MagicMock, context: Context, mocked_storage: None, track_names: list[str]
) -> None:
    updaters.tracks.add_tracks_by_name(track_names)
    assert not context.storage.tracks_to_download
