from progress.bar import ChargingBar
from page_loader.logger import logging_info
from pathlib import Path
from page_loader.resource_downloader import download_resources, CHUNK_SIZE
from page_loader.resource_downloader import get_path
import os
import logging
import requests


HTML_EXT = '.html'


@logging_info('Downloading html')
def download_html(url, file_path, client):
    logging.info('Requesting to %s', url)
    response = client.get(url, stream=True)
    response.raise_for_status()

    total_size = CHUNK_SIZE
    if response.headers.get('Content-Length'):
        total_size = int(response.headers.get('Content-Length'))

    try:
        with open(file_path, 'wb') as file:
            with ChargingBar(url, max=total_size / CHUNK_SIZE) as bar:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    file.write(chunk)
                    bar.next()
    except OSError:
        raise


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
