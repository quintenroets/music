import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from typing_extensions import Self

if TYPE_CHECKING:
    from spotdl.types.result import Result  # pragma: nocover

T = TypeVar("T", bound="Response")


@dataclass
class Response:
    name: str
    artists: tuple[str, ...]
    duration: float
    id: str

    @property
    def title(self) -> str:
        artists = ", ".join(self.artists)
        return artists + " - " + self.name

    @property
    def duration_message(self) -> str:
        duration = datetime.timedelta(seconds=self.duration)
        return str(duration).removeprefix("0:")

    @property
    def info(self) -> dict[str, str]:
        return {"title": self.title, "id": self.id, "duration": self.duration_message}

    @classmethod
    def from_result(cls, result: "Result") -> Self:
        return cls(
            artists=result.artists or (),
            name=result.name,
            duration=result.duration,
            id=result.result_id,
        )
