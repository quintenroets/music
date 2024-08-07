import contextlib


def test_ci_import() -> None:
    with contextlib.suppress(ModuleNotFoundError):
        from music.utils import ci_context  # noqa: F401
