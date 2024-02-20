from hypothesis import given, strategies
from music.models import Artist, ArtistType


@strategies.composite
def artist_strategy(draw: strategies.DrawFn) -> Artist:
    text_strategy = strategies.text()
    id_ = draw(text_strategy)
    name = draw(text_strategy)
    type_ = draw(strategies.sampled_from(ArtistType))
    return Artist(id_, name, type_)


@given(artist=artist_strategy())
def test_serialization(artist: Artist) -> None:
    artist_info = artist.dict()
    for value in artist_info.values():
        assert isinstance(value, str)
    assert Artist.from_dict(artist_info) == artist


@given(id_=strategies.text(), name=strategies.text())
def test_defaults(id_: str, name: str) -> None:
    artist = Artist(id_, name)
    assert artist.type_ == Artist.type_


@given(artist=artist_strategy())
def test_type_toggle(artist: Artist) -> None:
    type_ = artist.type_
    artist.toggle_type()
    assert artist.type_ != type_


@given(artist=artist_strategy())
def test_sort_index(artist: Artist) -> None:
    assert artist.sort_index
