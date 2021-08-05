from page_loader.logger import logging_info
from pathlib import Path
from page_loader.resource_downloader import download_resources
from page_loader.resource_downloader import get_path, download_file
import os
import logging
import requests


HTML_EXT = '.html'


@logging_info('Downloading html')
def download_html(url, file_path, client):
    logging.info('Requesting to %s', url)
    response = client.get(url, stream=True)
    response.raise_for_status()

    download_file(file_path, url, response)


def download(url, output_path=os.getcwd(), library=requests):
    if not url:
        raise ValueError

    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError(f'{output_path} does not exist')

    html_path = get_path(url, output_path)
    download_html(url, html_path, library)
    download_resources(html_path, url)

    return html_path
