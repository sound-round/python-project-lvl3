from urllib.parse import urlparse, urljoin
from os.path import split
from page_loader.support_functions import write_file, get_path, get_full_name
import logging
import requests


TAG_ATTRIBUTES = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)


def walk_resources(url, parsed_html, dir_path):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    files_for_download = []
    for tag, attr in TAG_ATTRIBUTES:
        links = parsed_html.find_all(tag)
        for link in links:
            source = link.get(attr)
            if not source:
                continue
            if urlparse(source).netloc and urlparse(source).netloc != netloc:
                continue
            source = urlparse(source).path
            full_url = urljoin(url + '/', source)
            file_name = get_full_name(full_url)
            logging.info('Requesting to %s', full_url)
            dir_name = split(dir_path)[1]
            source_path = get_path(file_name, dir_name)
            link[attr] = source_path

            files_for_download.append((file_name, full_url))
    return files_for_download


def save_resource(files, dir_path):
    for file in files:
        file_name, full_url = file
        file_path = get_path(file_name, dir_path)
        logging.info('Requesting to %s', full_url)
        response = requests.get(full_url, stream=True)
        response.raise_for_status()
        write_file(file_path, full_url, response)
