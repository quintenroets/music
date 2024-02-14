import typing
from unittest.mock import patch

from hypothesis import given, settings, strategies
from hypothesis.strategies import SearchStrategy
from music.models import Path
from music.utils.cached_file_content import CachedFileContent, cached_path_property


def dictionary_strategy() -> SearchStrategy[dict[str, str]]:
    text_strategy = strategies.text()
    return strategies.dictionaries(keys=text_strategy, values=text_strategy)


@given(content=dictionary_strategy())
@settings(max_examples=10)
def test_load_only_once(content: dict[str, str]) -> None:
    with Path.tempfile() as path:
        path.yaml = content
        cached_file_content = path.cached_content
        content = cached_file_content.__get__(None)  # type: ignore
        with patch("music.utils.cached_file_content.CachedFileContent.load") as load:
            assert cached_file_content.__get__(None) == content  # type: ignore
        load.assert_not_called()


@given(content=dictionary_strategy())
@settings(max_examples=10)
def test_default(content: dict[str, str]) -> None:
    with Path.tempfile() as path:
        cached_file_content = CachedFileContent(path, default=content)
        assert cached_file_content.__get__(None) == content


@given(content=dictionary_strategy())
@settings(max_examples=10)
def test_reload_after_file_write(content: dict[str, str]) -> None:
    with Path.tempfile() as path:
        cached_file_content = path.cached_content
        path.yaml = content
        with patch("music.utils.cached_file_content.CachedFileContent.load") as load:
            load.return_value = content
            assert cached_file_content.__get__(None) == content  # type: ignore
        load.assert_called_once()


@given(content=dictionary_strategy())
@settings(max_examples=10)
def test_no_reload_after_set(content: dict[str, str]) -> None:
    with Path.tempfile() as path:
        cached_file_content = path.cached_content
        with patch("music.utils.cached_file_content.CachedFileContent.load") as load:
            cached_file_content.__set__(None, content)  # type: ignore
            assert cached_file_content.__get__(None) == content  # type: ignore
        load.assert_not_called()


@given(content=dictionary_strategy(), content2=dictionary_strategy())
@settings(max_examples=10)
def test_decorator(content: dict[str, str], content2: dict[str, str]) -> None:
    with Path.tempfile() as path:

        class TestModel:
            @property
            @cached_path_property(path)
            def content(self) -> dict[str, str]:
                result = path.yaml
                return typing.cast(dict[str, str], result)

            @content.fget.setter  # noqa
            def content(self, content_: dict[str, str]) -> None:
                path.yaml = content_

        test_model = TestModel()
        test_model.content = content  # type: ignore
        assert test_model.content == content
        path.yaml = content2
        # tests are so quick to mtime needs to be increased manually
        path.mtime += 1
        assert test_model.content == content2
