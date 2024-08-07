from unittest.mock import MagicMock, patch

import pytest
from music.updaters import artists as artists_updater


@patch("music.clients.spotify.Client.album_count", return_value=1)
@pytest.mark.usefixtures("_mocked_storage", "artist")
def test_check_for_new_songs(mocked_album_count: MagicMock) -> None:
    artists_updater.check_for_new_songs()
    with patch("music.updaters.artist.ArtistUpdater.check_albums") as check_albums:
        artists_updater.check_for_new_songs()
    check_albums.assert_not_called()
    mocked_album_count.assert_called()
