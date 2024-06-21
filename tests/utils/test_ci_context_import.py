def test_ci_import() -> None:
    try:
        from music.utils import ci_context  # noqa: F401
    except ModuleNotFoundError:  # pragma: nocover
        pass
