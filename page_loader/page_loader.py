# from pathlib import Path
from page_loader.resource_downloader import download_resources
from page_loader.html_downloader import get_html_path, download_html
import os


def download(url, output_path=os.getcwd()):
    if not url:
        raise ValueError

    # TODO discuss
    # directory = Path(output_path)
    # if not directory.is_dir():
    #    raise FileNotFoundError(f'{output_path} does not exist')

    html_path = get_html_path(url, output_path)
    download_html(url, html_path)
    download_resources(html_path, url)

    return html_path
