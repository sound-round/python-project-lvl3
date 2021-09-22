from progress.bar import ChargingBar
from os.path import join, splitext
from urllib.parse import urlparse
import re
import logging


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
CHUNK_SIZE = 1024
HTML_EXT = '.html'
DIR_ENDING = '_files'


def get_full_name(url, type=None):
    parsed_url = urlparse(url)
    file_name, file_ext = splitext(parsed_url.path)
    formatted_path = format_name(parsed_url.netloc + file_name).strip("-")
    if type == 'dir':
        return f'{formatted_path}{file_ext}{DIR_ENDING}'
    if not file_ext or type == 'html':
        return f'{formatted_path}{file_ext}{HTML_EXT}'
    return f'{formatted_path}{file_ext}'  # TODO splitext на последнюю часть


def get_path(full_file_name, output_path):
    return join(output_path, full_file_name)


def format_name(file_name, replacer='-'):
    formatted_file_name = re.sub(FORBIDDEN_CHARS, replacer, file_name).lower()
    return formatted_file_name


def write_file(file_path, url, response):
    total_size = CHUNK_SIZE
    if response.headers.get('Content-Length'):
        total_size = int(response.headers.get('Content-Length'))
    with open(file_path, 'wb') as file:
        with ChargingBar(url, max=total_size / CHUNK_SIZE) as bar:
            logging.info('Downloading chunks')
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)
                bar.next()
