from progress.bar import ChargingBar
import re
import logging


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
CHUNK_SIZE = 1024


def format_name(file_name):
    formatted_file_name = re.sub(FORBIDDEN_CHARS, '-', file_name).lower()
    if formatted_file_name[-1] == '-':
        formatted_file_name = formatted_file_name[:-1]
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
