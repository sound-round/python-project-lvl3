from pathlib import Path
from page_loader.common import get_path
from page_loader.logger import logging_info
from page_loader.resource_downloader \
    import get_resources_data, download_resource
from os.path import splitext
from bs4 import BeautifulSoup
import os
import requests
import logging


def get_download_dir_path(html_path):
    root, _ = splitext(html_path)
    return root + '_files'


@logging_info('Creating download directory')
def create_download_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


@logging_info('Downloading resources')
def parse_html(html_file):
    logging.debug('Parsing html')
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    return parsed_html


def write_html(parsed_html, html_path):
    logging.debug('Rewriting html')
    with open(html_path, 'w') as file:
        file.write(parsed_html.prettify(formatter="html5"))


def download(url, output_path=os.getcwd()):
    if not url:
        raise ValueError

    directory = Path(output_path)
    if not directory.is_dir() and not directory.is_file():
        raise FileNotFoundError(f'{output_path} does not exist')

    html_path = get_path(url, output_path)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    html_file = response.content

    download_dir_path = get_download_dir_path(html_path)
    create_download_dir(download_dir_path)

    parsed_html = parse_html(html_file)
    resources_data = get_resources_data(parsed_html)
    for resource_data in resources_data:
        download_resource(url, resource_data, download_dir_path)
    write_html(parsed_html, html_path)

    return html_path
