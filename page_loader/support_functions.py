from os.path import join, splitext
from urllib.parse import urlparse
import re


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'
CHUNK_SIZE = 1024
HTML_EXT = '.html'
DIR_ENDING = '_files'


def get_full_name(url, type=None):
    parsed_url = urlparse(url)
    file_name, file_ext = splitext(parsed_url.path)
    formatted_path = format_name(parsed_url.netloc + file_name)
    if type == 'dir':
        return f'{formatted_path}{DIR_ENDING}'
    if not file_ext:
        return f'{formatted_path}{HTML_EXT}'
    return f'{formatted_path}{file_ext}'


def get_path(full_file_name, output_path):
    return join(output_path, full_file_name)


def format_name(file_name, replacer='-'):
    formatted_file_name = re.sub(FORBIDDEN_CHARS, replacer, file_name).lower()
    return formatted_file_name
