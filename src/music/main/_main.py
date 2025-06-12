from music import updaters
import cli
from music.models import Path
from music.runtime import runtime


def main() -> None:
    """
    Download new songs.
    """
    if runtime.ci_context is not None:  # pragma: nocover
        with runtime.ci_context:
            _main()
    else:
        _main()


def _main() -> None:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time

    # Set up headless browser (optional: remove headless to debug)
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Visit the video or homepage to get cookies
    url = "https://www.youtube.com/watch?v=Q--Wk-5sXDA"
    driver.get(url)
    time.sleep(3)  # wait for cookies to be set

    # Extract cookies
    cookies = driver.get_cookies()
    driver.quit()

    # Write in Netscape format
    with open("cookies.txt", "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie["domain"]
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = cookie["path"]
            secure = "TRUE" if cookie["secure"] else "FALSE"
            expiration = str(int(cookie.get("expiry", 9999999999)))
            name = cookie["name"]
            value = cookie["value"]
            f.write(
                f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}\n"
            )
    cli.run("cat cookies.txt")

    command = (
        "yt-dlp https://music.youtube.com/watch?v=Q--Wk-5sXDA --cookies cookies.txt"
    )
    cli.run(command)
    return
    if runtime.context.options.clean_download_ids:
        updaters.download_ids.clean_download_ids()
    else:
        collect_new_songs()


def collect_new_songs() -> None:
    upload_to_phone = should_upload_to_phone()
    if not upload_to_phone and not runtime.storage.tracks_ready_for_download:
        updaters.artists.check_for_new_songs()
    print(runtime.storage.tracks_to_download)
    if runtime.storage.tracks_ready_for_download:
        download_new_songs()
        upload_to_phone = should_upload_to_phone()
    if upload_to_phone:
        upload_new_downloads()


def should_upload_to_phone() -> bool:
    processed_songs_present = not Path.processed_songs.is_empty()
    return runtime.context.options.upload_to_phone and processed_songs_present


def download_new_songs() -> None:
    # lazy import for performance
    from music.download import download_new_songs

    download_new_songs.download_new_songs()


def upload_new_downloads() -> None:
    # lazy import for performance
    from . import uploader

    uploader.start()
