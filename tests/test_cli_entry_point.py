import pytest
from music import cli


@pytest.mark.skip()
def test_testing() -> None:
    cli.entry_point()
