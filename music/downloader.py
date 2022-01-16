import cli
import requests
import sys

from retry import retry

from .datamanager import DataManager
from .path import Path


class Downloader:
    @staticmethod
    def download(new_songs):
        output_path = Path.downloaded_songs
        output_path.mkdir(parents=True, exist_ok=True)
        for p in output_path.glob('*'):
            p.unlink() # existing downloads raise errors
        
        options = {
            'output-format': 'opus',
            'output': output_path,
            'download-threads': 10,
            'search-threads': 10
        }
        songs = [
            id_ if 'http' in id_ else f'https://open.spotify.com/track/{id_}' for id_ in new_songs
        ]

        prev_songs = None
        while songs and prev_songs != songs:
            Downloader.run('spotdl', options, songs)
            prev_songs = songs
            songs = list(output_path.glob('*.spotdlTrackingFile'))

    @staticmethod
    @retry(requests.exceptions.ReadTimeout)
    def run(*args):
        try:
            cli.run(*args)
        except requests.exceptions.ReadTimeout:
            cli.run('clear')
            raise
