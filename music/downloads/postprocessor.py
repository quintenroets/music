import calendar
from datetime import datetime

from mutagen import oggopus

import music


def process_downloads():
    for download in music.Path.downloaded_songs.glob("*.opus"):
        if download.size == 0:
            raise Exception(f"{download} is empty file")
        else:
            process_download(download)


def process_download(download, first_time=True):
    tags = oggopus.OggOpus(download)

    title = tags["title"][0]
    time = parse_time(tags)
    new_title = (
        f"{title} | {calendar.month_name[time.month][:3]} {time.day}, {time.year}"
    )
    tags["title"] = new_title

    if first_time:
        tags.save()
        download.rename(music.Path.processed_songs / download.name)

    # do this after all other operations to avoid resetting mtime
    download.mtime = max(time.timestamp(), 0)


def parse_time(tags):
    date = tags["date"][0]
    parts = date.split("-")
    if len(parts) == 1:
        parts += [1, 1]

    y, m, d = parts
    y, m, d = int(y), int(m), int(d)
    return datetime(y, m, d)
