import random

from music import Path
from music.artist.artist import Artist
from music.artist.artists import Artists
from music.client import spotapi
from music.downloads import jobs


class ArtistManager:
    @staticmethod
    def artists():
        artists = Artists()
        infos = spotapi.artists(artists.ids)
        artists = artists.artist_list()
        infos = [info.dict() | a.dict() for a, info in zip(artists, infos)]
        return infos

    @staticmethod
    def add_artist(id, name):
        artist = Artist(id, name)
        artists = Artists()
        artists[id] = artist
        artists.save()

    @staticmethod
    def add_song(id):
        tracks = spotapi.songs([id])
        jobs.add(tracks)

    @staticmethod
    def search_artists(name):
        artists = Artists()
        search_results = spotapi.search_artist(name)
        search_results = [
            s.dict() | {"added": s.id in artists.artists} for s in search_results
        ]
        return search_results

    @staticmethod
    def search_song(name):
        songs = spotapi.search_song(name)
        downloads = Path.download_ids.content
        songs = [s.dict() | {"downloaded": jobs.is_downloaded(s)} for s in songs]
        return songs

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
            artists = [a for a in spotapi.related_artists(id) if a.id not in ids]
            recommendations.update(artists)
            for artist in artists:
                freqs[artist.id] = freqs.get(artist.id, 0) + 1

        Path.recommendations.content = freqs
        recommendations = sorted(recommendations, key=lambda r: freqs[r.id])
        return recommendations
