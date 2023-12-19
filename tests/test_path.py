from collections.abc import Iterator

import pytest
from hypothesis import HealthCheck, given, settings, strategies
from hypothesis.strategies import SearchStrategy
from music.backend.utils import Path

NestedDict = dict[str, dict[str, str]]


def dictionary_strategy() -> SearchStrategy[dict[str, str]]:
    return strategies.dictionaries(keys=strategies.text(), values=strategies.text())


def nested_dictionary_generator() -> SearchStrategy[NestedDict]:
    return strategies.dictionaries(
        keys=strategies.text(),
        values=dictionary_strategy(),
    )


@pytest.fixture()  # type: ignore
def path() -> Iterator[Path]:
    with Path.tempfile() as path:
        yield path
    path.json_path.unlink(missing_ok=True)
    for removed_path in (path, path.json_path):
        assert not removed_path.exists()


@given(content=nested_dictionary_generator())  # type: ignore
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), max_examples=10)  # type: ignore
def test_yaml(path: Path, content: NestedDict) -> None:
    path.yaml = content
    assert path.yaml == content


@given(content=nested_dictionary_generator())  # type: ignore
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), max_examples=10)  # type: ignore
def test_json_usage(path: Path, content: NestedDict) -> None:
    path.json_path.json = content
    assert path.yaml == content


@given(content1=nested_dictionary_generator(), content2=nested_dictionary_generator())  # type: ignore
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), max_examples=10)  # type: ignore
def test_yaml_priority(path: Path, content1: NestedDict, content2: NestedDict) -> None:
    path.yaml = content1
    path.json_path.json = content2
    path.json_path.mtime = path.mtime - 1
    assert path.yaml == content1
