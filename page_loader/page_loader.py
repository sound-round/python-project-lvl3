from page_loader.common import format_name
from urllib.parse import urlparse
from os.path import join
from page_loader.logger import logging_info
from page_loader.resource_downloader import download_resources
from os.path import splitext
from bs4 import BeautifulSoup
import os
import requests
import logging


HTML_EXT = '.html'


def get_html_path(url, output_path):
    parsed_url = urlparse(url)
    file_name = f'{parsed_url.netloc}{parsed_url.path}'
    formatted_file_name = format_name(file_name)
    return join(output_path, formatted_file_name) + HTML_EXT


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


def rewrite_html(parsed_html, html_path):
    logging.debug('Rewriting html')
    with open(html_path, 'w') as file:
        file.write(parsed_html.prettify(formatter="html5"))


def download(url, output_path=os.getcwd()):
    if not url:
        raise ValueError

    html_path = get_html_path(url, output_path)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    html_file = response.content

    download_dir_path = get_download_dir_path(html_path)
    create_download_dir(download_dir_path)

    parsed_html = parse_html(html_file)
    download_resources(parsed_html, url, download_dir_path)
    rewrite_html(parsed_html, html_path)

    return html_path
