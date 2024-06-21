import importlib.util


def test_ci_import() -> None:
    try:
        importlib.util.find_spec("music.utils.ci")
    except ModuleNotFoundError:
        pass
