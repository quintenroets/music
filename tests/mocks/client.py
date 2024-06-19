from typing import Any, cast

from music.models import Path

data_root: Path = Path.source_root.parent.parent / "tests" / "mocks" / "data"


def internal_call(
    _: Any, __: str, url: str, ___: dict[str, str], params: dict[str, Any]
) -> dict[str, str] | None:
    name: Path | str
    url_parts = url.split("/")
    if len(url_parts) == 2 and url_parts[0] in ("albums", "artists", "tracks"):
        name = data_root.subpath(*url_parts)
        if not name.with_suffix(".json").exists():
            name = name.with_name(url_parts[0])
    elif url == "search":
        type_ = params["type"]
        name = f"search-{type_}"
    elif url == "recommendations":
        name = url
    elif url.endswith("top-tracks"):
        name = "top-tracks"
    elif url.startswith("artists"):
        name = "related-artists" if url.endswith("related-artists") else "artist-albums"
    else:
        raise ValueError(f"No mock for {url}")
    path = (data_root / name).with_suffix(".json")
    return cast(dict[str, Any], path.json)
