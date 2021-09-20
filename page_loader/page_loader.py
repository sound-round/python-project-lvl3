from pathlib import Path
from page_loader.support_functions import get_path, get_full_name
from page_loader.logger import logging_info
from page_loader.resource_downloader \
    import get_resources, format_resource, save_resource
from bs4 import BeautifulSoup
import os
import requests
import logging


@logging_info('Creating download directory')
def create_download_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


@logging_info('Parsing html')
def parse_html(html_file):
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    return parsed_html


def write_html(parsed_html, html_path):
    with open(html_path, 'w') as file:
        file.write(parsed_html)


def download(url, output_path=os.getcwd()):

    directory = Path(output_path)
    if not directory.is_dir() and not directory.is_file():
        raise FileNotFoundError(f'Directory {output_path} does not exist')

    html_name = get_full_name(url)
    html_path = get_path(html_name, output_path, type='html')
    download_dir_path = get_path(html_name, output_path, type='dir')
    response = requests.get(url, stream=True)
    response.raise_for_status()
    html_file = response.content
    create_download_dir(download_dir_path)

    logging.debug('Parsing html')
    parsed_html = parse_html(html_file)

    resources = get_resources(parsed_html)
    for resource in resources:
        save_resource(url, resource, download_dir_path)
        format_resource(url, resource, download_dir_path)

    logging.info('Writing html')
    write_html(parsed_html.prettify(formatter="html5"), html_path)

    return html_path
