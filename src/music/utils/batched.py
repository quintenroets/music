from collections.abc import Iterator
from typing import TypeVar

T = TypeVar("T")


def batched(items: list[T], size: int = 50) -> Iterator[list[T]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]
