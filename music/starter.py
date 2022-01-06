import sys
import os

from libs import env
from .path import Path

env.load(path=Path.env)  # load env here before it is used in other files

from libs.errorhandler import ErrorHandler
from libs.output import Output
from libs.progressbar import ProgressBar

from .artistmanager import ArtistManager
from .datamanager import DataManager
from .downloader import Downloader
from .postprocessor import PostProcessor
from .uploader import Uploader

class Starter:
    @staticmethod
    def start():
        Path.assets.mkdir(parents=True, exist_ok=True)
        os.chdir(Path.assets) # for log files
        
        if "add" in sys.argv:
            new_songs = {url: "" for url in sys.argv[2:]}
            DataManager.add_new_songs(new_songs)
        elif "download" not in sys.argv and not Path.songs.load():
            with Output(capture_errors=True):
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
        artists = DataManager.get_artists()
        artists = ProgressBar(artists, title="Music", message="Checking new songs", progress_name="artists")

        new_songs = {
            song["id"]: f'{song["name"]} - {song["artists"][0]["name"]}'
            for artist in artists for song in ArtistManager.check_updates(artist)
        }

        if new_songs:
            DataManager.add_new_songs(new_songs)

    @staticmethod
    def process_new_songs(new_songs):
        print(f"{len(new_songs)} new songs")
        Downloader.download(new_songs)
        PostProcessor.process_downloads()
        Uploader.start()
        DataManager.remove_new_songs(new_songs)


def main():
    with ErrorHandler():
        from libs.timer import Timer
        with Timer():
            if "upload" in sys.argv:
                Uploader.start()
            else:
                Starter.start()

if __name__ == "__main__":
    main()
