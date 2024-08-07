from collections.abc import Iterable
from typing import TypeVar

import cli

T = TypeVar("T")


def track_progress(
    sequence: Iterable[T],
    description: str = "",
    unit: str = "item",
    total: int | None = None,
    *,
    cleanup_after_finish: bool = True,
) -> Iterable[T]:
    yield from cli.track_progress(
        sequence,
        description,
        unit,
        total,
        cleanup_after_finish=cleanup_after_finish,
    )
