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

    url = "https://www.youtube.com/watch?v=Q--Wk-5sXDA"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(10)  # allow page to fully render & bot checks to clear

    cookies = driver.get_cookies()
    driver.quit()

    with open("cookies.txt", "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for c in cookies:
            domain = c["domain"]
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = c["path"]
            secure = "TRUE" if c["secure"] else "FALSE"
            expires = str(int(c.get("expiry", 9999999999)))
            name = c["name"]
            value = c["value"]
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n")
    cli.run("cat cookies.txt")

    path = Path.secrets.parent / "cookies.txt"
    command = f'yt-dlp -vvv https://youtube.com/watch?v=Q--Wk-5sXDA --print-traffic --cookies {path} --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36"'
    print(command)
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
