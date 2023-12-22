from typing import Any, TypeVar

import plib

T = TypeVar("T")


class BasePath(plib.Path):  # type: ignore
    @property
    def yaml(self) -> dict[str, Any] | int:
        # cache results in json
        if self.json_path.mtime < self.mtime:
            self.json_path.json = super().yaml
        return self.json_path.json  # type: ignore

    @yaml.setter
    def yaml(self, value: dict[str, Any] | int) -> None:
        super(plib.Path, plib.Path(self)).__setattr__("yaml", value)
        self.json_path.json = value

    @property
    def json_path(self: T) -> T:
        return self.with_suffix(".json")  # type: ignore


class Path(BasePath):
    assets: BasePath = BasePath.assets / "music"

    download_info = assets / "downloads"
    download_ids = download_info / "ids.yaml"
    fails = download_info / "fails.yaml"
    to_download = assets / "cache" / "to_download.yaml"
    frontend_assets = assets / "frontend"
    frontend_hash = frontend_assets / "source_code_hash.txt"

    artist_assets = assets / "artists"
    artists = artist_assets / "artists.yaml"
    recommendations = artist_assets / "recommendations.yaml"

    config = assets / "config" / "config.yaml"

    tokens = assets / "tokens" / "tokens"
    cache_assets = assets / "cache"
    cache = cache_assets / ".cache"

    download_assets: BasePath = BasePath("/") / "media" / "backup" / "Music"
    downloaded_songs = download_assets / "downloads"
    processed_songs = download_assets / "processed"
    all_songs = download_assets / "all"
    deleted = download_assets / "deleted"

    root = BasePath(__file__).parent.parent.parent
    frontend = root / "frontend"

    phone = "Music"
