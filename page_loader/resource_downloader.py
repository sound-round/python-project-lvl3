from progress.bar import ChargingBar
from page_loader.logger import logging_info
from urllib.parse import urlparse, urljoin
from os.path import split, splitext, join
from bs4 import BeautifulSoup
import os
import re
import logging
import requests


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
CHUNK_SIZE = 1024
TAGS_AND_ATTRIBUTES = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)
HTML_EXT = '.html'


def format_name(file_name):
    formatted_file_name = re.sub(FORBIDDEN_CHARS, '-', file_name).lower()
    if formatted_file_name[-1] == '-':
        formatted_file_name = formatted_file_name[:-1]
    return formatted_file_name


def get_path(url, output_path):
    parsed_url = urlparse(url)
    file_name, file_ext = splitext(f'{parsed_url.netloc}{parsed_url.path}')
    if not file_ext:
        file_ext = HTML_EXT
    formatted_file_name = format_name(file_name)
    return join(output_path, formatted_file_name) + file_ext


@logging_info('Creating download directory')
def create_download_dir(html_path):
    root, _ = splitext(html_path)
    dir_path = root + '_files'
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            raise
    return dir_path


@logging_info('Getting input data')
def get_resources_data(file, tags_and_attributes):

    # get pairs of links(list) and tag
    resources_data = []
    for tag, attr in tags_and_attributes:
        links = file.find_all(tag)
        resources_data.append((links, attr))
    return resources_data


def walk_links(url, resource_data, dir_path):
    links, attr = resource_data
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    domain_name = f'{parsed_url.scheme}://{netloc}'
    for link in links:
        source = link.get(attr)
        if not source:
            continue
        if urlparse(source).netloc and urlparse(source).netloc != netloc:
            continue
        if urlparse(source).netloc == netloc:
            source = urlparse(source).path
        url = urljoin(domain_name, source)

        file_path = get_path(url, dir_path)
        logging.info('Requesting to %s', url)
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = CHUNK_SIZE
        if response.headers.get('Content-Length'):
            total_size = int(response.headers.get('Content-Length'))

        try:
            with open(file_path, 'wb') as file:
                with ChargingBar(url, max=total_size/CHUNK_SIZE) as bar:
                    logging.debug('Downloading chunks')
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        file.write(chunk)
                        bar.next()
        except OSError:
            raise

        dir_name = split(dir_path)[1]
        source_path = get_path(url, dir_name)
        link[attr] = source_path


@logging_info('Downloading resources')
def download_resources(html_path, url):
    try:
        html_file = open(html_path, 'r')
    except IOError:
        raise

    logging.debug('Parsing html')
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    resources_data = get_resources_data(parsed_html, TAGS_AND_ATTRIBUTES)
    dir_path = create_download_dir(html_path)

    for resource_data in resources_data:
        walk_links(url, resource_data, dir_path)

    logging.debug('Closing html')
    html_file.close()

    logging.debug('Rewriting html')
    try:
        with open(html_path, 'wb') as file:
            file.write(parsed_html.encode(formatter="html5"))
    except IOError:
        raise
