from music.backend.utils import Path


def main():
    Path.to_download.unlink()  # disable cache file
    todo = Path.to_download.yaml
    print(len(todo))
    downloads = [p.stem.lower() for p in Path.all_songs.iterdir()]
    download_titles = [map(d) for d in downloads]
    new_todo = {
        k: v for k, v in todo.items() if not found(v, downloads, download_titles)
    }
    Path.to_download.yaml = new_todo
    print(len(new_todo))


def found(v, downloads, download_titles):
    if v.lower() in downloads:
        return True

    if map(v) in download_titles:
        print(v)
        print(downloads[download_titles.index(map(v))])
        if input():
            return True

    return False


def map(value):
    return " - ".join(value.split(" - ")[1:]).lower()


if __name__ == "__main__":
    main()
