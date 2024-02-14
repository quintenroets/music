import functools
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def combine_chunks(f: Callable[..., list[T]]) -> Callable[..., list[T]]:
    """
    Combine function calls on chunks instead of whole array in one time :return: All
    results of the chunks.
    """

    @functools.wraps(f)
    def chunked_wrapper(*args: Any, **kwargs: Any) -> list[T]:
        self, items, *args_tuple = args

        @combine_offsets
        def calculate_chunk(self: Any, offset: int, limit: int) -> list[T]:
            return f(self, items[offset : offset + limit], *args_tuple, **kwargs)

        return calculate_chunk(self, len(items))

    return chunked_wrapper


def combine_offsets(
    f: Callable[..., list[T]], chunk_size: int = 50
) -> Callable[..., list[T]]:
    """
    Combine function calls with offset and limit instead of total amount :param
    chunk_size: Size of the chunks :return: All results of the chunks.
    """

    def chunked_wrapper(self: Any, amount: int, *args: Any, **kwargs: Any) -> list[T]:
        return [
            item
            for offset in range(0, amount, chunk_size)
            for item in f(self, *args, offset=offset, limit=chunk_size, **kwargs)
        ]

    return chunked_wrapper
