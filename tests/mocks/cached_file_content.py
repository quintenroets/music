import time
import typing
from dataclasses import dataclass
from typing import Any, ClassVar, Generic, TypeVar

from package_utils.storage import cached_file_content
from plib import Path

T = TypeVar("T")


@dataclass
class CachedFileContent(cached_file_content.CachedFileContent[T], Generic[T]):
    _storage: ClassVar[dict[Path, Any]] = {}

    def __get__(self, instance: Any, owner: type[Any] | None = None) -> T:
        if self.load_function is None:
            untyped_result = CachedFileContent._storage.get(self.path, self.default)
            result = typing.cast(T, untyped_result)
        else:
            result = self.load_function(instance)
        return result

    def __set__(self, instance: Any, value: T) -> None:
        if self.save_function is None:
            CachedFileContent._storage[self.path] = value
        else:
            self.save_function(instance, value)  # pragma: nocover
        self.mtime = time.time()
