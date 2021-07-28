import requests
from urllib.parse import urlparse
import re
from pathlib import Path
import os
from os.path import split, splitext, join
from bs4 import BeautifulSoup
import logging

FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
TAGS_AND_ATTRIBUTES = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)


def download_html(url, file_path, client):
    try:
        logging.info('Requesting to %s', url)
        response = client.get(url, stream=True)
    except (requests.ConnectionError, requests.HTTPError) as e:
        print(e)
        logging.error(e)
    else:
        with open(file_path, 'wb') as file:
            logging.debug('Downloading chunks')
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)


def create_download_dir(html_path):
    root, _ = splitext(html_path)
    dir_path = root + '_files'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def get_input_data(source, tags_and_attributes):

    # get pairs of links(list) and tag
    input_data = []
    logging.debug('Getting input data')
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
        image_path = join(dir_path, formatted_file_name) + file_ext
        print('✓', url)

        logging.info('Requesting to %s', url)
        response = requests.get(url, stream=True)

        with open(image_path, 'wb') as file:
            logging.debug('Downloading chunks')
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        logging.info('%s is downloaded', url)

        source_path = join(dir_name, formatted_file_name) + file_ext
        link[attr] = source_path


def download_resources(html_path, dir_path, domain_name, netloc):
    directory = Path(dir_path)
    if not directory.is_dir():
        logging.error(FileNotFoundError)
        raise FileNotFoundError
    file_path = Path(html_path)
    if not file_path:
        logging.error(FileNotFoundError)
        raise FileNotFoundError

    logging.debug('Opening html to download resources')
    html_file = open(html_path, 'r')

    logging.debug('Parsing html')
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    all_input_data = get_input_data(parsed_html, TAGS_AND_ATTRIBUTES)

    for input_data in all_input_data:
        walk_links(input_data, domain_name, netloc, dir_path)
    logging.info('All resources are downloaded')
    logging.debug('Closing html')
    html_file.close()

    logging.debug('Rewriting html')
    with open(html_path, 'wb') as file:
        file.write(parsed_html.encode(formatter="html5"))


def download(url, output_path=os.getcwd(), library=requests):

    logging.info('Starting download...')

    if not url:
        logging.info(ValueError)
        raise ValueError

    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError
    parsed_url = urlparse(url)
    html_name = f'{parsed_url.netloc}{parsed_url.path}'
    formatted_html_name = re.sub(FORBIDDEN_CHARS, '-', html_name).lower()
    if formatted_html_name[-1] == '-':
        formatted_html_name = formatted_html_name[:-1]
    html_path = f'{output_path}/{formatted_html_name}{".html"}'

    logging.info('Downloading html...')
    download_html(url, html_path, library)
    logging.info('Downloading html finished')

    logging.info('Creating downloading directory...')
    download_dir_path = create_download_dir(html_path)
    logging.info('Downloading directory created')

    domain_name = f'{parsed_url.scheme}://{parsed_url.netloc}'

    logging.info('Downloading resources...')
    download_resources(
        html_path,
        download_dir_path,
        domain_name,
        parsed_url.netloc
    )

    return html_path
