from unittest.mock import MagicMock, patch

import pytest

from music import updaters
from music.context import Context
from music.models.response_types import Track


@pytest.fixture
def track_names(track: Track) -> list[str]:
    return [track.name]


@patch("cli.confirm", return_value=True)
@pytest.mark.usefixtures("_mocked_storage")
def test_tracks_confirmed(
    mocked_confirm: MagicMock,
    context: Context,
    track: Track,
) -> None:
    names = [track.name]
    updaters.tracks.add_tracks_by_name(names)
    assert track.id in context.storage.tracks_to_download
    mocked_confirm.assert_called()


@patch("cli.confirm", return_value=False)
@pytest.mark.usefixtures("_mocked_storage")
def test_tracks_not_confirmed(
    mocked_confirm: MagicMock,
    context: Context,
    track_names: list[str],
) -> None:
    updaters.tracks.add_tracks_by_name(track_names)
    assert not context.storage.tracks_to_download
    mocked_confirm.assert_called()
