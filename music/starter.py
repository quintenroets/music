import cli
import music
import os
import sys

from .artistmanager import ArtistManager
from .data import Data
from .datamanager import DataManager
from .uploader import Uploader


class Starter:
    @staticmethod
    def start():
        music.Path.assets.mkdir(parents=True, exist_ok=True)
        os.chdir(music.Path.assets) # for log files
        
        if 'add' in sys.argv:
            new_songs = {url: '' for url in sys.argv[2:]}
            DataManager.add_new_songs(new_songs)
        elif 'download' not in sys.argv and not music.Path.songs.content:
            Starter.check_new_songs()

        new_songs = music.Path.songs.load()

        chunck_size = 50
        iterations = 1

        for _ in range(iterations):
            new_songs = {k: new_songs[k] for k in list(new_songs.keys())[:chunck_size]}
            if new_songs:
                Starter.process_new_songs(new_songs)

    @staticmethod
    def check_new_songs():
        all_downloads = music.Path.downloads.load()

        artists = Data.artists()
        artists = cli.progress(artists, description='Checking new songs', unit='artists')
        new_songs = {}
        
        for artist in artists:
            for song in ArtistManager.check_updates(artist):
                id_ = song['id']
                if id_ not in all_downloads:
                    new_songs[id_] = f'{song["name"]} - {song["artists"][0]["name"]}'
                    cli.console.print(new_songs[id_])

        if new_songs:
            DataManager.add_new_songs(new_songs)

    @staticmethod
    def process_new_songs(new_songs):
        music.download(new_songs)
        music.process_downloads()
        Uploader.start()
        DataManager.remove_new_songs(new_songs)


def main():
    if 'upload' in sys.argv:
        Uploader.start()
    else:
        Starter.start()
    if 'hang' in sys.argv:
        print('Press key to exit')
        input('$ ')

if __name__ == '__main__':
    main()
