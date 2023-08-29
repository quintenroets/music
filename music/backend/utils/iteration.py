def chunked(items, chunk_size=50):
    for i in range(0, len(items), chunk_size):
        yield items[i : i + chunk_size]
