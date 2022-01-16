import random

from .datamanager import DataManager
from .path import Path
from .spotapi import SpotApi

class ArtistManager:
    @staticmethod
    def save(type_, id_, name):
        artist = {
            'type': type_,
            'id': id_,
            'name': name
        }
        DataManager.add_artist(artist)

    @staticmethod
    def get_recommended_artists(required_amount=50, max_tries=10):
        ids = DataManager.get_artist_ids()
        random.shuffle(ids)

        freqs = Path.recommendations.load()
        new_ids = []
        recommendations = []

        for seed_id in ids[: max_tries]:
            if len(recommendations) < required_amount:

                new_recommendations = SpotApi.get_recommended_artists(seed_id)
                for rec in new_recommendations:
                    id_ = rec['id']
                    if id_ not in ids:
                        if id_ not in new_ids:
                            new_ids.append(id_)
                            recommendations.append(rec)
                            freqs[id_] = freqs.get(id_, 0) + 1 # increase freq

        Path.recommendations.save(freqs)
        recommendations = sorted(recommendations, key=lambda rec: freqs[rec['id']])

        return recommendations

    @staticmethod
    def check_updates(artist):
        all = artist['type'] == 'favorite'
        return DataManager.get_new_songs(artist, all=all)
