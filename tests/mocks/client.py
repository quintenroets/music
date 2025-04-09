from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from typing import Any, cast

from music.models import Path

data_root: Path = Path.source_root.parent.parent / "tests" / "mocks" / "data"


def mock_internal_call(
    _: Any,
    __: str,
    url: str,
    ___: dict[str, str],
    params: dict[str, Any],
) -> dict[str, str] | None:
    return Mocker(url, params).mock_internal_call()


@dataclass
class Mocker:
    url: str
    params: dict[str, Any]
    ids_keyword: str = "?ids="

    @cached_property
    def url_parts(self) -> list[str]:
        return [part for part in self.url.split("/") if part]

    @cached_property
    def group(self) -> str:
        return self.url_parts[0]

    @cached_property
    def id_part(self) -> str:
        return self.url_parts[1]

    def mock_internal_call(self) -> dict[str, Any] | None:
        return (
            self.mock_artists()
            if self.group == "artists" and self.has_id and self.has_multiple_ids
            else self._mock_internal_call()
        )

    def mock_artists(self) -> dict[str, list[dict[str, str]]] | None:
        def generate_artists() -> Iterator[dict[str, str]]:
            ids = self.determine_id_path().name.split("_")
            for id_ in ids:
                path = data_root / "artist" / id_
                path = path.with_suffix(".json")
                assert path.exists()
                content = path.json
                yield cast("dict[str, str]", content)

        return {"artists": list(generate_artists())}

    def _mock_internal_call(self) -> dict[str, str | list[dict[str, str]]] | None:
        path: Path | str
        if self.has_id:
            path = self.determine_id_path()
        elif self.url == "search":
            type_ = self.params["type"]
            path = f"search-{type_}"
        elif self.url == "recommendations":
            path = self.url
        elif self.url.endswith("top-tracks"):
            path = "top-tracks"
        elif self.group == "artists":
            path = (
                "related-artists"
                if self.url.endswith("related-artists")
                else "artist-albums"
            )
        elif self.group == "albums" and self.url_parts[-1] == "tracks":
            path = "album-songs"
        else:  # pragma: nocover
            message = f"No mock for {self.url}"
            raise ValueError(message)
        path = (data_root / path).with_suffix(".json")
        assert path.exists()
        return cast("dict[str, Any]", path.json)

    def determine_id_path(self) -> Path:
        id_ = (
            self.id_part.split(self.ids_keyword)[1].replace(",", "_")
            if self.has_multiple_ids
            else self.id_part
        )
        group = self.group if self.has_multiple_ids else self.group[:-1]
        return data_root / group / id_

    @property
    def has_multiple_ids(self) -> bool:
        return self.ids_keyword in self.id_part

    @property
    def has_id(self) -> bool:
        group_with_id = ("albums", "tracks", "artists")
        return len(self.url_parts) == 2 and self.group in group_with_id
