import calendar
import mutagen
from mutagen.oggopus import OggOpus
from mutagen.id3 import ID3, USLT
from mutagen.easyid3 import EasyID3
from pathlib import Path

from mutagen.oggopus import OggOpus
from time import mktime

from libs.time import set_time
from libs.progressbar import ProgressBar

from .datamanager import DataManager
from .lyricsmanager import LyricsManager


class PostProcessor:
    @staticmethod
    def process_downloads():
        downloads = DataManager.get_downloaded_songs()
        iterator = ProgressBar(downloads, title="Music", message="postprocessing", progress_name="songs")

        for download in iterator:
            if download.stat().st_size == 0:
                download.unlink()
            else:
                PostProcessor.process(download)

    @staticmethod
    def process(filename):
        tags = mutagen.oggopus.OggOpus(filename)

        title = tags["title"][0]

        if "|" not in title:
            day, month, year = PostProcessor.get_time(tags)
            month = calendar.month_name[month][:3]
            timestring = month + " " + str(day) + ", " + str(year)
            new_title = title + " | " + timestring
            tags["title"] = new_title
            tags.save()

            PostProcessor.set_time(filename, tags)

    def check_lyrics(filename, tags):
        artist = tags["artist"][0]
        title = tags["title"][0]
        lyrics = tags["lyrics"][0] if "lyrics" in tags.keys() else None

        if not lyrics:
            print(f"Adding lyrics for {title} by {artist}")
            lyrics = LyricsManager.get_lyrics(artist, title)
            if len(lyrics) < 200 or len(lyrics) > 10000 or lyrics.count("_") > 80:
                return

        audiofile = ID3(filename)
        audiofile["USLT"] = USLT(encoding=3, desc=u"Lyrics", text=lyrics)
        audiofile.save(v2_version=3)

    @staticmethod
    def set_time(filename, audiofile):
        day, month, year = PostProcessor.get_time(audiofile)

        timestamp = (year, month, day, 0, 0, 0, 0, 0, 0)
        timestamp = mktime(timestamp)
        set_time(filename, timestamp)

    @staticmethod
    def get_time(tags):
        date = tags["date"]

        if date:
            date = date[0]

            year = date.split("-")[0]
            date = date.replace(year, "")

            if date and date[0] == "-":
                date = date[1:]
            month = date.split("-")[0]

            date = date.replace(month, "")
            if date and date[0] == "-":
                date = date[1:]

            day = date.split("-")[0]

            year = int(year) if year else None
            month = int(month) if month else 1
            day = int(day) if day else 1

            return day, month, year
