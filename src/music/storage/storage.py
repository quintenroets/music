from collections.abc import Iterator
from functools import cached_property

import cli
from package_utils.storage import cached_path_property

from ..models import Artist, Path
from ..models.response_types import Track


class Storage:
    downloaded_tracks: dict[str, str] = Path.download_ids.cached_content
    tracks_to_download: dict[str, str] = Path.to_download.cached_content
    recommendation_frequencies: dict[str, float] = Path.recommendations.cached_content

    @property
    def artists(self) -> list[Artist]:
        return self._artists

    @artists.setter
    def artists(self, value: list[Artist]) -> None:
        self._artists = value  # type: ignore

    @property
    @cached_path_property(Path.artists)
    def _artists(self) -> list[Artist]:
        return [Artist.from_dict(artist) for artist in Path.artists.yaml]

    @_artists.fget.setter  # noqa
    def _artists(self, artists: list[Artist]) -> None:
        # use sort_index explicitly because dataclass ordering does not work
        artists = sorted(artists, key=lambda artist: artist.sort_index)
        Path.artists.yaml = [artist.dict() for artist in artists]

    def save_new_artist(self, artist: Artist) -> None:
        self.artists = self.artists + [artist]

    @property
    @cached_path_property(Path.artists)
    def artist_ids(self) -> set[str]:
        return set(artist.id for artist in self.artists)

    @property
    @cached_path_property(Path.artists)
    def artists_per_id(self) -> dict[str, Artist]:
        return {artist.id: artist for artist in self.artists}

    def get_artist(self, id: str) -> Artist:
        return self.artists_per_id[id]

    @cached_property
    def downloaded_track_names(self) -> set[str]:
        names = self.downloaded_tracks.values()
        return set(names)

    @cached_property
    def downloaded_track_ids(self) -> set[str]:
        ids = self.downloaded_tracks.keys()
        return set(ids)

    @property
    def ids_to_download(self) -> list[str]:
        ids = self.tracks_to_download.keys()
        return list(ids)

    def save_new_tracks(self, tracks: list[Track]) -> None:
        tracks_to_download = self._extract_tracks_to_download(tracks)
        tracks_mapping = {track.id: track.full_name for track in tracks_to_download}
        if tracks_mapping:
            self.tracks_to_download |= tracks_mapping

    def _extract_tracks_to_download(self, tracks: list[Track]) -> Iterator[Track]:
        tracks = sorted(tracks, key=lambda track_: track_.popularity, reverse=True)
        for track in tracks:
            if self._should_download(track):
                cli.console.print(track.full_name)
                yield track

    def _should_download(self, track: Track) -> bool:
        """
        A new track has a non-existing:
        - id
        - full name
        because the same song can occur with:
        - different id's: different album
        - different full name: different artists
        """
        return (
            track.should_download
            and track.id not in self.downloaded_track_ids
            and track.full_name not in self.downloaded_track_names
        )
