import typing
from types import TracebackType
from typing import Any, TypeVar

import superpathlib
from simple_classproperty import classproperty

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @property  # type: ignore
    def yaml(self) -> dict[str, Any] | int:
        # cache results in json
        if self.json_path.mtime < self.mtime:
            self.json_path.json = super().yaml
        return self.json_path.json  # type: ignore

    @yaml.setter
    def yaml(self, value: dict[str, Any] | int) -> None:
        super(superpathlib.Path, superpathlib.Path(self)).__setattr__("yaml", value)
        self.json_path.json = value  # type: ignore

    @property
    def json_path(self: T) -> T:
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
    def source_root(cls: type[T]) -> T:
        return cls(__file__).parent.parent

    @classmethod
    @classproperty
    def assets(cls: type[T]) -> T:
        path = cls.script_assets / cls.source_root.name
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def config(cls: type[T]) -> T:
        path = cls.assets / "config" / "config.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def download_info(cls: type[T]) -> T:
        path = cls.assets / "downloads"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def download_ids(cls: type[T]) -> T:
        path = cls.download_info / "ids.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def fails(cls: type[T]) -> T:
        path = cls.download_info / "fails.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def to_download(cls: type[T]) -> T:
        path = cls.assets / "cache" / "to_download.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def artist_assets(cls: type[T]) -> T:
        path = cls.assets / "artists"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def artists(cls: type[T]) -> T:
        path = cls.artist_assets / "artists.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def recommendations(cls: type[T]) -> T:
        path = cls.artist_assets / "recommendations.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def secrets(cls: type[T]) -> T:
        # don't use json caching here
        path = superpathlib.Path(cls.assets) / "tokens" / "tokens"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def cache_assets(cls: type[T]) -> T:
        path = cls.assets / "cache"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def cache(cls: type[T]) -> T:
        path = cls.cache_assets / ".cache"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def download_assets(cls: type[T]) -> T:
        return cls("/") / "media" / "backup" / "Music"

    @classmethod
    @classproperty
    def downloaded_songs(cls: type[T]) -> T:
        path = cls.download_assets / "downloads"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def processed_songs(cls: type[T]) -> T:
        path = cls.download_assets / "processed"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def all_songs(cls: type[T]) -> T:
        path = cls.download_assets / "all"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def deleted(cls: type[T]) -> T:
        path = cls.download_assets / "deleted"
        return typing.cast(T, path)

    phone = "Music"
