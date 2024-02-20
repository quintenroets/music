from unittest.mock import patch

from music.models import Artist
from music.updaters import artists as artists_updater


@patch("music.clients.spotify.Client.album_count", return_value=1)
def test_check_for_new_songs(artist: Artist, mocked_storage: None) -> None:
    artists_updater.check_for_new_songs()

    with patch("music.updaters.artist.ArtistUpdater.check_albums") as check_albums:
        artists_updater.check_for_new_songs()
    check_albums.assert_not_called()
