import pytest
from hypothesis import HealthCheck, given, settings, strategies

from music.backend.utils import Path


def dictionary_strategy():
    return strategies.dictionaries(keys=strategies.text(), values=strategies.text())


def nested_dictionary_generator():
    return strategies.dictionaries(
        keys=strategies.text(),
        values=dictionary_strategy(),
    )


@pytest.fixture()
def path():
    with Path.tempfile() as path:
        yield path
    path.json_path.unlink(missing_ok=True)
    for removed_path in (path, path.json_path):
        assert not removed_path.exists()


@given(content=nested_dictionary_generator())
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), max_examples=10)
def test_yaml(path, content):
    path.yaml = content
    assert path.yaml == content


@given(content=nested_dictionary_generator())
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), max_examples=10)
def test_json_usage(path, content):
    path.json_path.json = content
    assert path.yaml == content


@given(content1=nested_dictionary_generator(), content2=nested_dictionary_generator())
@settings(suppress_health_check=(HealthCheck.function_scoped_fixture,), max_examples=10)
def test_yaml_priority(path, content1, content2):
    path.yaml = content1
    path.json_path.json = content2
    path.json_path.mtime = path.mtime - 1
    assert path.yaml == content1
