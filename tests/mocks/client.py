from typing import Any, cast

from music.models import Path

data_root: Path = Path.source_root.parent.parent / "tests" / "mocks" / "data"


def internal_call(
    _: Any,
    __: str,
    url: str,
    ___: dict[str, str],
    params: dict[str, Any],
) -> dict[str, str] | None:
    path: Path | str
    url_parts = [part for part in url.split("/") if part]
    group = url_parts[0]
    if len(url_parts) == 2 and group in ("albums", "artists", "tracks"):
        path = determine_id_path(url_parts)
    elif url == "search":
        type_ = params["type"]
        path = f"search-{type_}"
    elif url == "recommendations":
        path = url
    elif url.endswith("top-tracks"):
        path = "top-tracks"
    elif group == "artists":
        path = "related-artists" if url.endswith("related-artists") else "artist-albums"
    elif group == "albums" and url_parts[-1] == "tracks":
        path = "album-songs"
    else:  # pragma: nocover
        message = f"No mock for {url}"
        raise ValueError(message)
    path = (data_root / path).with_suffix(".json")
    assert path.exists()
    return cast(dict[str, Any], path.json)


def determine_id_path(url_parts: list[str]) -> Path:
    group = url_parts[0]
    id_part = url_parts[1]
    ids_keyword = "?ids="
    id_ = (
        id_part.split(ids_keyword)[1].replace(",", "_")
        if ids_keyword in id_part
        else id_part
    )
    if ids_keyword not in url_parts[1]:
        group = group[:-1]
    return data_root / group / id_
