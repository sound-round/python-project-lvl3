from progress.bar import ChargingBar
from os.path import join, splitext
from urllib.parse import urlparse
import re
import logging


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
CHUNK_SIZE = 1024
HTML_EXT = '.html'
REPLACER = '-'
DIR_ENDING = '_files'


def get_path(url, output_path, file_type=''):
    parsed_url = urlparse(url)
    full_file_name = f'{parsed_url.netloc}{parsed_url.path}'

    if file_type == 'dir':
        return join(output_path, format_name(full_file_name)) + DIR_ENDING

    file_name, file_ext = splitext(full_file_name)
    if not file_ext:
        file_type = 'html'

    if file_type == 'html':
        file_ext = HTML_EXT
        return join(output_path, format_name(full_file_name)) + file_ext

    return join(output_path, format_name(file_name)) + file_ext


def format_name(file_name):
    if file_name[-1] == '/':
        file_name = file_name[:-1]
    formatted_file_name = re.sub(FORBIDDEN_CHARS, REPLACER, file_name).lower()
    return formatted_file_name


def download_file(file_path, url, response):
    total_size = CHUNK_SIZE
    if response.headers.get('Content-Length'):
        total_size = int(response.headers.get('Content-Length'))
    with open(file_path, 'wb') as file:
        with ChargingBar(url, max=total_size / CHUNK_SIZE) as bar:
            logging.debug('Downloading chunks')
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)
                bar.next()
