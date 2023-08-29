import random
from dataclasses import dataclass

from music.backend.artist import Artist, Artists
from music.backend.artist.artists import artists as artists_collection
from music.backend.client import response_types, spotapi
from music.backend.downloads import jobs
from music.backend.utils import Path


@dataclass
class DisplaySong(response_types.Track):
    downloaded: bool = False

    @classmethod
    def from_track(cls, track: response_types.Track):
        # don't use dict() method because it serializes all attributes recursively
        attributes = track.__dict__
        attributes["downloaded"] = jobs.is_downloaded(track)
        return DisplaySong(**attributes)


@dataclass
class DisplayArtist(response_types.ArtistInfo):
    added: bool = False

    @classmethod
    def from_artist_info(cls, artist: response_types.ArtistInfo):
        attributes = artist.__dict__
        attributes["added"] = artist.id in artists_collection.artists
        return DisplayArtist(**attributes)


def artists():
    artists = Artists()
    infos = spotapi.artists(artists.ids)
    artists = artists.artist_list()
    infos = [info.dict() | a.dict() for a, info in zip(artists, infos)]
    return infos


def add_artist(id, name):
    artists = Artists()
    artists[id] = Artist(id, name)
    artists.save()


def add_song(id):
    tracks = spotapi.songs([id])
    jobs.add(tracks)


def search_artists(name):
    return [
        DisplayArtist.from_artist_info(artist) for artist in spotapi.search_artist(name)
    ]


def search_song(name):
    return [DisplaySong.from_track(song) for song in spotapi.search_song(name)]
    # TODO: add youtube songs if spotify result list is empty


def change_artist(id: str):
    artists = Artists()
    artists[id].toggle_type()
    artists.save()


def recommendations(amount=50, max_tries=10):
    ids = Artists().ids
    random.shuffle(ids)
    seed_ids = ids[:max_tries]

    freqs = Path.recommendations.yaml
    recommendations = set({})

    while len(recommendations) < amount and seed_ids:
        id = seed_ids.pop(0)
        artists = [a for a in spotapi.related_artists(id) if a.id not in ids]
        recommendations.update(artists)
        for artist in artists:
            freqs[artist.id] = freqs.get(artist.id, 0) + 1

    Path.recommendations.yaml = freqs
    recommendations = sorted(recommendations, key=lambda r: freqs[r.id])
    return recommendations


def song_recommendations(seed_amount=5):
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
