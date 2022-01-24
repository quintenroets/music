import random

from music.artist.artist import Artist
from music.artist.artists import Artists
from music import Path
from music.client import spotapi


class ArtistManager:
    @staticmethod
    def artists():
        artists = Artists()
        artists_info = spotapi.artists(artists.ids)
        for a, info in zip(artists, artists_info):
            info |= a.dict()

        return artists_info

    @staticmethod
    def add_artist(id, name):
        artist = Artist(id, name)
        artists = Artists()
        artists[id] = artist
        artists.save()

    @staticmethod
    def search_artists(name):
        artists = Artists()
        search_results = spotapi.search_artist(name)
        for r in search_results:
            r.added = r.id in artists
        return search_results

    @staticmethod
    def change_artist(id):
        artists = Artists()
        artists[id].chage()
        artists.save()

    @staticmethod
    def recommendations(amount=50, max_tries=10):
        ids = Artists().ids
        random.shuffle(ids)
        seed_ids = ids[:max_tries]

        freqs = Path.recommendations.content
        recommendations = set({})

        while len(recommendations) < amount and seed_ids:
            id = seed_ids.pop(0)
            artists = spotapi.related_artists(id)
            recommendations.update(artists)
            for artist in artists:
                freqs[artist.id] = freqs.get(artist.id, 0) + 1

        Path.recommendations.content = freqs
        recommendations = sorted(recommendations, key=lambda r: freqs[r.id])
        return recommendations
