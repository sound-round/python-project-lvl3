from page_loader.logger import logging_info
from pathlib import Path
from page_loader.resource_downloader import download_resources
from page_loader.resource_downloader import download_file
from urllib.parse import urlparse
from os.path import join
from page_loader.resource_downloader import format_name
import os
import logging
import requests


HTML_EXT = '.html'


def get_html_path(url, output_path):
    parsed_url = urlparse(url)
    file_name = f'{parsed_url.netloc}{parsed_url.path}'
    formatted_file_name = format_name(file_name)
    return join(output_path, formatted_file_name) + HTML_EXT


@logging_info('Downloading html')
def download_html(url, file_path, client=requests):
    logging.info('Requesting to %s', url)
    response = client.get(url, stream=True)
    response.raise_for_status()
    logging.info(f'html_path: {file_path}')
    download_file(file_path, url, response)


def download(url, output_path=os.getcwd()):  # TODO delete library
    if not url:
        raise ValueError

    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError(f'{output_path} does not exist')

    html_path = get_html_path(url, output_path)
    download_html(url, html_path)
    download_resources(html_path, url)

    return html_path
