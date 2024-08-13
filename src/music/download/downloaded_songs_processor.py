import calendar
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import cached_property

from mutagen import oggopus

from music.models import Path


def run() -> None:
    for path in Path.downloaded_songs.glob("*.opus"):
        if path.size == 0:
            message = f"{path} is empty file"
            raise RuntimeError(message)
        DownloadedTrackProcessor(path).run()


@dataclass
class DownloadedTrackProcessor:
    path: Path
    set_title: bool = True

    def __post_init__(self) -> None:
        self.metadata = oggopus.OggOpus(self.path)  # type: ignore[no-untyped-call]

    def run(self) -> None:
        if self.set_title:
            self.add_title_metadata()
        # do this after all other operations to avoid resetting mtime
        self.path.mtime = max(self.mtime.timestamp(), 0)
        self.move_to_processed_songs()

    def move_to_processed_songs(self) -> None:
        self.path.rename(Path.processed_songs / self.path.name)

    def add_title_metadata(self) -> None:
        month = calendar.month_name[self.mtime.month][:3]
        date_ = f"{month} {self.mtime.day}, {self.mtime.year}"
        title = self.metadata["title"][0]
        self.metadata["title"] = f"{title} | {date_}"
        self.metadata.save()

    @cached_property
    def mtime(self) -> datetime:
        date = self.metadata["date"][0]
        parts = date.split("-")
        if len(parts) == 1:
            parts += [1, 1]  # pragma: nocover

        year, month, day = parts
        year_int, month_int, day_int = int(year), int(month), int(day)
        return datetime(year_int, month_int, day_int, tzinfo=timezone.utc)
