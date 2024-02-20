from hypothesis import given, settings, strategies
from hypothesis.strategies import SearchStrategy
from music.models.path import Path


def text_dictionary_strategy() -> SearchStrategy[dict[str, str]]:
    return strategies.dictionaries(keys=strategies.text(), values=strategies.text())


def dictionary_strategy() -> SearchStrategy[dict[str, dict[str, str]]]:
    return strategies.dictionaries(
        keys=strategies.text(),
        values=text_dictionary_strategy(),
    )


dictionary_content = given(content=dictionary_strategy())


def test_paths() -> None:
    paths = (
        Path.config,
        Path.download_ids,
        Path.fails,
        Path.to_download,
        Path.artists,
        Path.recommendations,
        Path.secrets,
        Path.cache,
        Path.downloaded_songs,
        Path.processed_songs,
        Path.all_songs,
        Path.deleted,
        Path.phone,
    )
    unique_paths = set(paths)
    assert len(paths) == len(unique_paths)


@dictionary_content
@settings(max_examples=10)
def test_yaml(content: dict[str, dict[str, str]]) -> None:
    with Path.tempfile() as path:
        path.yaml = content
        assert path.yaml == content


@dictionary_content
@settings(max_examples=10)
def test_json(content: dict[str, dict[str, str]]) -> None:
    with Path.tempfile() as path:
        path.json = content
        assert path.json == content


@dictionary_content
@settings(max_examples=10)
def test_json_cache(content: dict[str, dict[str, str]]) -> None:
    with Path.tempfile() as path:
        path.json_path.json = content
        assert path.yaml == content


@given(content=dictionary_strategy(), content2=dictionary_strategy())
@settings(max_examples=10)
def test_yaml_priority(
    content: dict[str, dict[str, str]], content2: dict[str, dict[str, str]]
) -> None:
    with Path.tempfile() as path:
        path.json_path.json = content
        path.yaml = content2
        path.mtime = path.json_path.mtime + 1
        assert path.yaml == content2
