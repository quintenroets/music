from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any


@contextmanager
def mocked_method(
    object_class: type[Any], name: str, new_method: Callable[..., Any]
) -> Iterator[None]:
    restored_method = getattr(object_class, name)
    setattr(object_class, name, new_method)
    try:
        yield
    finally:
        setattr(object_class, name, restored_method)
