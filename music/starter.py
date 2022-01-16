import cli
import os
import sys
from tqdm import tqdm

from .artistmanager import ArtistManager
from .datamanager import DataManager
from .downloader import Downloader
from .path import Path
from .postprocessor import PostProcessor
from .uploader import Uploader


class Starter:
    @staticmethod
    def start():
        Path.assets.mkdir(parents=True, exist_ok=True)
        os.chdir(Path.assets) # for log files
        
        if 'add' in sys.argv:
            new_songs = {url: '' for url in sys.argv[2:]}
            DataManager.add_new_songs(new_songs)
        elif 'download' not in sys.argv and not Path.songs.load():
            Starter.check_new_songs()

        new_songs = Path.songs.load()

        chunck_size = 50
        iterations = 1

        for _ in range(iterations):
            new_songs = {k: new_songs[k] for k in list(new_songs.keys())[:chunck_size]}
            if new_songs:
                Starter.process_new_songs(new_songs)

    @staticmethod
    def check_new_songs():
        all_downloads = Path.downloads.load()
        
        artists = DataManager.get_artists()
        progress_format = '|{bar}| {n_fmt}/{total_fmt} artists [{elapsed}<{remaining}]'
        progress = tqdm(artists, unit='artists', bar_format=progress_format)
        desc = tqdm(bar_format='{desc}')
        new_songs = {}
        count = 0
        
        with desc, progress:
            for artist in artists:
                progress.update()
                width = os.get_terminal_size().columns if sys.stdout.isatty() else 0
                desc.desc = f'  {count} new songs: checking {artist["name"]}..'.ljust(width)
                desc.refresh()
                
                for song in ArtistManager.check_updates(artist):
                    id_ = song['id']
                    if id_ not in all_downloads:
                        new_songs[id_] = f'{song["name"]} - {song["artists"][0]["name"]}'
                        count += 1
            desc.desc = f'  {count} new songs'
            desc.refresh()

        if new_songs:
            DataManager.add_new_songs(new_songs)

    @staticmethod
    def process_new_songs(new_songs):
        Downloader.download(new_songs)
        PostProcessor.process_downloads()
        Uploader.start()
        DataManager.remove_new_songs(new_songs)


def main():
    with cli.errorhandler():
        if 'upload' in sys.argv:
            Uploader.start()
        else:
            Starter.start()

if __name__ == '__main__':
    main()
