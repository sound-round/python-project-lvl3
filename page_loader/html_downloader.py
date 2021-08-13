from page_loader.logger import logging_info
from page_loader.common import download_file, format_name
from urllib.parse import urlparse
from os.path import join
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
