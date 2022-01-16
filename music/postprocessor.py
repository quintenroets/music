import calendar
from datetime import datetime
from mutagen import oggopus

from .datamanager import DataManager


class PostProcessor:
    @staticmethod
    def process_downloads():
        downloads = DataManager.get_downloaded_songs()

        for download in downloads:
            if download.size == 0:
                download.unlink()
            else:
                PostProcessor.process(download)

    @staticmethod
    def process(filename):
        tags = oggopus.OggOpus(filename)

        title = tags['title'][0]

        if '|' not in title:
            time = PostProcessor.parse_time(tags)
            filename.time = time.timestamp()
            
            month = calendar.month_name[time.month][:3]
            tags['title'] = f'{title} | {month} {time.day}, {time.year}'
            tags.save()

    @staticmethod
    def parse_time(tags):
        date = tags['date'][0]
        parts = date.split('-')
        if len(parts) < 1:
            parts += [1, 1]
        
        y, m, d = parts
        y, m, d = int(y), int(m), int(d)
        return datetime(y, m, d)
