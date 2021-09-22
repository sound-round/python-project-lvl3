from page_loader.support_functions import get_path, get_full_name
from page_loader.logger import logging_info
from page_loader.resource_downloader \
    import walk_resources, save_resource
from bs4 import BeautifulSoup
import os
import requests
import logging


@logging_info('Creating download directory')
def create_download_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


@logging_info('Parsing html')
def parse_html(html_file):
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    return parsed_html


def write_html(parsed_html, html_path):
    logging.debug(str(parsed_html))
    with open(html_path, 'w') as file:
        file.write(parsed_html)


def download(url, output_path=os.getcwd()):

    html_name = get_full_name(url, type='html')
    download_dir_name = get_full_name(url, type='dir')
    html_path = get_path(html_name, output_path)
    download_dir_path = get_path(download_dir_name, output_path,)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    html_file = response.content
    create_download_dir(download_dir_path)

    logging.info('Parsing html')
    parsed_html = parse_html(html_file)

    files_for_download = walk_resources(url, parsed_html, download_dir_path)
    save_resource(files_for_download, download_dir_path)

    logging.info('Writing html')
    write_html(parsed_html.prettify(formatter="html5"), html_path)

    return html_path

# 3. C тестами разобраться.
