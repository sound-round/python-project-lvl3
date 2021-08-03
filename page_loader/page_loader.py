from progress.bar import ChargingBar
from page_loader.logger import logging_info
from pathlib import Path
from urllib.parse import urlparse
from os.path import split, splitext, join
from bs4 import BeautifulSoup
import os
import re
import logging
import requests


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
TAGS_AND_ATTRIBUTES = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)
CHUNK_SIZE = 1024


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


def get_path(url, output_path):
    parsed_url = urlparse(url)
    file_name = f'{parsed_url.netloc}{parsed_url.path}'
    formatted_file_name = re.sub(FORBIDDEN_CHARS, '-', file_name).lower()
    if formatted_file_name[-1] == '-':
        formatted_file_name = formatted_file_name[:-1]
    return join(output_path, formatted_file_name) + ".html"


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
def get_input_data(source, tags_and_attributes):

    # get pairs of links(list) and tag
    input_data = []
    for tag, attr in tags_and_attributes:
        links = source.find_all(tag)
        input_data.append((links, attr))
    return input_data


def walk_links(input_data, domain_name, netloc, dir_path):
    links, attr = input_data
    dir_name = split(dir_path)[1]
    for link in links:
        source = link.get(attr)
        if not source:
            continue
        if urlparse(source).netloc and urlparse(source).netloc != netloc:
            continue
        if urlparse(source).netloc == netloc:
            source = urlparse(source).path
        # url = join(domain_name, source)
        url = f'{domain_name}{source}'
        file_name, file_ext = splitext(f'{netloc}{source}')
        if not file_ext:
            file_ext = '.html'
        formatted_file_name = re.sub(FORBIDDEN_CHARS, '-', file_name).lower()
        if formatted_file_name[-1] == '-':
            formatted_file_name = formatted_file_name[:-1]
        file_path = join(dir_path, formatted_file_name) + file_ext

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

        source_path = join(dir_name, formatted_file_name) + file_ext
        link[attr] = source_path


@logging_info('Downloading resources')
def download_resources(html_path, domain_name, netloc):
    try:
        html_file = open(html_path, 'r')
    except IOError:
        raise

    logging.debug('Parsing html')
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    all_input_data = get_input_data(parsed_html, TAGS_AND_ATTRIBUTES)
    dir_path = create_download_dir(html_path)
    for input_data in all_input_data:
        walk_links(input_data, domain_name, netloc, dir_path)

    logging.debug('Closing html')
    html_file.close()

    logging.debug('Rewriting html')
    try:
        with open(html_path, 'wb') as file:
            file.write(parsed_html.encode(formatter="html5"))
    except IOError:
        raise


def download(url, output_path=os.getcwd(), library=requests):
    if not url:
        raise ValueError

    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError(f'{output_path} does not exist')

    html_path = get_path(url, output_path)
    download_html(url, html_path, library)

    parsed_url = urlparse(url)
    domain_name = f'{parsed_url.scheme}://{parsed_url.netloc}'

    download_resources(
        html_path,
        domain_name,
        parsed_url.netloc
    )

    return html_path
