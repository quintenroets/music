from types import TracebackType
from typing import Any, TypeVar, cast

import superpathlib
from simple_classproperty import classproperty
from typing_extensions import Self

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @property  # type: ignore[override]
    def yaml(self) -> dict[str, Any] | int:
        # cache results in json
        if self.json_path.mtime < self.mtime:
            self.json_path.json = super().yaml
        return self.json_path.json  # type: ignore[return-value]

    @yaml.setter
    def yaml(self, value: dict[str, Any] | int) -> None:
        super(superpathlib.Path, superpathlib.Path(self)).__setattr__("yaml", value)
        self.json_path.json = value  # type: ignore[assignment]

    @property
    def json_path(self) -> Self:
        return self.with_suffix(".json")

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        super().__exit__(exception_type, exception_value, traceback)
        super(Path, self.json_path).__exit__(exception_type, exception_value, traceback)

    @classmethod
    @classproperty
    def source_root(cls) -> Self:
        return cls(__file__).parent.parent

    @classmethod
    @classproperty
    def assets(cls) -> Self:
        path = cls.script_assets / cls.source_root.name
        return cast("Self", path)

    @classmethod
    @classproperty
    def config(cls) -> Self:
        path = cls.assets / "config" / "config.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def download_info(cls) -> Self:
        path = cls.assets / "downloads"
        return cast("Self", path)

    @classmethod
    @classproperty
    def download_ids(cls) -> Self:
        path = cls.download_info / "ids.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def fails(cls) -> Self:
        path = cls.download_info / "fails.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def to_download(cls) -> Self:
        path = cls.cache_assets / "to_download.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def to_download_youtube(cls) -> Self:
        path = cls.download_info / "to_download_youtube.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def artist_assets(cls) -> Self:
        path = cls.assets / "artists"
        return cast("Self", path)

    @classmethod
    @classproperty
    def artists(cls) -> Self:
        path = cls.artist_assets / "artists.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def recommendations(cls) -> Self:
        path = cls.artist_assets / "recommendations.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def secrets(cls) -> Self:
        # don't use json caching here
        path = superpathlib.Path(cls.assets) / "tokens" / "tokens"
        return cast("Self", path)

    @classmethod
    @classproperty
    def cache_assets(cls) -> Self:
        path = cls.assets / "cache"
        return cast("Self", path)

    @classmethod
    @classproperty
    def cache(cls) -> Self:
        path = cls.cache_assets / ".cache"
        return cast("Self", path)

    @classmethod
    @classproperty
    def download_assets(cls) -> Self:
        return cls("/") / "media" / "backup" / "Music"

    @classmethod
    @classproperty
    def downloaded_songs(cls) -> Self:
        path = cls.download_assets / "downloads"
        return cast("Self", path)

    @classmethod
    @classproperty
    def processed_songs(cls) -> Self:
        path = cls.download_assets / "processed"
        return cast("Self", path)

    @classmethod
    @classproperty
    def all_songs(cls) -> Self:
        path = cls.download_assets / "all"
        return cast("Self", path)

    @classmethod
    @classproperty
    def deleted(cls) -> Self:
        path = cls.download_assets / "deleted"
        return cast("Self", path)

    phone = "Music"
