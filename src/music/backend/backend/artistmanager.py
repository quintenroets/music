from __future__ import annotations

import random
from dataclasses import dataclass

from ..artist import Artist, Artists
from ..artist.artists import artists as artists_collection
from ..client import response_types, spotapi
from ..client.response_types import ArtistInfo, Track
from ..downloads import jobs
from ..utils import Path


@dataclass
class DisplaySong(response_types.Track):
    downloaded: bool = False

    @classmethod
    def from_track(cls, track: response_types.Track) -> DisplaySong:
        # don't use dict() method because it serializes all attributes recursively
        attributes = track.__dict__
        attributes["downloaded"] = jobs.is_downloaded(track)
        return DisplaySong(**attributes)


@dataclass
class DisplayArtist(response_types.ArtistInfo):
    added: bool = False

    @classmethod
    def from_artist_info(cls, artist: response_types.ArtistInfo) -> DisplayArtist:
        attributes = artist.__dict__
        attributes["added"] = artist.id in artists_collection.artists
        return DisplayArtist(**attributes)


def artists() -> list[dict[str, str]]:
    loaded_artists = Artists()
    api_infos = spotapi.artists(loaded_artists.ids)
    loaded_artists_list = loaded_artists.artist_list()
    infos = [info.dict() | a.dict() for a, info in zip(loaded_artists_list, api_infos)]
    return infos


def add_artist(id: str, name: str) -> None:
    loaded_artists = Artists()
    artist = Artist(id, name)
    loaded_artists.add(artist)
    loaded_artists.save()


def add_song(id: str) -> None:
    tracks = spotapi.songs([id])
    jobs.add(tracks)


def search_artists(name: str) -> list[DisplayArtist]:
    return [
        DisplayArtist.from_artist_info(artist) for artist in spotapi.search_artist(name)
    ]


def search_song(name: str) -> list[DisplaySong]:
    return [DisplaySong.from_track(song) for song in spotapi.search_song(name)]
    # TODO: add youtube songs if spotify result list is empty


def change_artist(id: str) -> None:
    loaded_artists = Artists()
    loaded_artists[id].toggle_type()
    loaded_artists.save()


def recommendations(amount: int = 50, max_tries: int = 10) -> list[ArtistInfo]:
    ids = Artists().ids
    random.shuffle(ids)
    seed_ids = ids[:max_tries]

    freqs = Path.recommendations.yaml
    artist_recommendations: set[ArtistInfo] = set({})

    while len(artist_recommendations) < amount and seed_ids:
        id = seed_ids.pop(0)
        recommended_artists = [
            a for a in spotapi.related_artists(id) if a.id not in ids
        ]
        artist_recommendations.update(recommended_artists)
        for artist in recommended_artists:
            freqs[artist.id] = freqs.get(artist.id, 0) + 1

    Path.recommendations.yaml = freqs
    artist_recommendations_list = sorted(
        list(artist_recommendations), key=lambda r: freqs[r.id]
    )
    return artist_recommendations_list


def song_recommendations(seed_amount: int = 5) -> list[Track]:
    downloads = Path.download_ids.yaml
    ids = list(downloads.keys())
    random.shuffle(ids)
    seed_ids = ids[:seed_amount]

    names = {v for v in downloads.values()}
    songs = [
        s
        for s in spotapi.song_recommendations(seed_ids)
        if s.id not in downloads and jobs.full_name(s) not in names
    ]
    return songs
