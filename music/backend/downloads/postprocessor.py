import calendar
from datetime import datetime

from mutagen import oggopus

from ..utils import Path


def process_downloads():
    for download in Path.downloaded_songs.glob("*.opus"):
        if download.size == 0:
            raise Exception(f"{download} is empty file")
        else:
            process_download(download)


def process_download(download, set_title=True):
    tags = oggopus.OggOpus(download)

    title = tags["title"][0]
    time = parse_time(tags)

    if set_title:
        new_title = (
            f"{title} | {calendar.month_name[time.month][:3]} {time.day}, {time.year}"
        )
        tags["title"] = new_title
        tags.save()

    # do this after all other operations to avoid resetting mtime
    download.mtime = max(time.timestamp(), 0)
    download.rename(Path.processed_songs / download.name)


def parse_time(tags):
    date = tags["date"][0]
    parts = date.split("-")
    if len(parts) == 1:
        parts += [1, 1]

    y, m, d = parts
    y, m, d = int(y), int(m), int(d)
    return datetime(y, m, d)
