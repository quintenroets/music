import plib


class BasePath(plib.Path):
    @property
    def yaml(self) -> dict:
        # cache results in json
        if self.json_path.mtime < self.mtime:
            self.json_path.json = super().yaml
        return self.json_path.json

    @yaml.setter
    def yaml(self, value):
        super(plib.Path, plib.Path(self)).__setattr__("yaml", value)
        self.json_path.json = value

    @property
    def json_path(self):
        return self.with_suffix(".json")


class Path(BasePath):
    assets: BasePath = BasePath.assets / "music"

    download_info = assets / "downloads"
    download_ids = download_info / "ids.yaml"
    fails = download_info / "fails.yaml"
    to_download = assets / "cache" / "to_download.yaml"

    artist_assets = assets / "artists"
    artists = artist_assets / "artists.yaml"
    recommendations = artist_assets / "recommendations.yaml"

    tokens = assets / "tokens" / "tokens"
    cache_assets = assets / "cache"
    cache = cache_assets / ".cache"

    download_assets: BasePath = BasePath.docs / "Backup" / "Music"
    downloaded_songs = download_assets / "downloads"
    processed_songs = download_assets / "processed"
    all_songs = download_assets / "all"
    deleted = download_assets / "deleted"

    root = BasePath(__file__).parent.parent
    frontend = root / "frontend" / "dist"

    phone = "Music"
