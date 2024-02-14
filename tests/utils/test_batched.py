from music.utils.batched import batched


def test_batched() -> None:
    items = list(range(50))
    batches = batched(items, size=5)
    batches_list = list(batches)
    assert len(batches_list) == 10
    assert (len(batch) == 5 for batch in batches_list)
