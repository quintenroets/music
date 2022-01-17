import calendar
import music
from datetime import datetime
from mutagen import oggopus


def process_downloads():
    for download in music.Path.downloaded_songs.glob('*.opus'):
        if download.size == 0:
            raise Exception(f'{download} is empty file')
        
        tags = oggopus.OggOpus(download)

        title = tags['title'][0]
        time = parse_time(tags)
        download.time = time.timestamp()
        tags['title'] = f'{title} | {calendar.month_name[time.month][:3]} {time.day}, {time.year}'
        tags.save()
        
        download.rename(music.Path.processed_songs / download.name)


def parse_time(tags):
    date = tags['date'][0]
    parts = date.split('-')
    if len(parts) == 1:
        parts += [1, 1]
    
    y, m, d = parts
    y, m, d = int(y), int(m), int(d)
    return datetime(y, m, d)
