from urllib.parse import urlparse, urljoin
from os.path import split
from progress.bar import ChargingBar
from page_loader.logger import logging_info
from page_loader.support_functions import get_path, get_full_name, CHUNK_SIZE
import requests


TAG_ATTRIBUTES = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)


def find_resources_for_download(url, parsed_html, dir_path):
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
            link[attr] = get_path(file_name, split(dir_path)[1])

            files_for_download.append((file_name, full_url))
    return files_for_download


def save_resource(resource, dir_path):
    file_name, full_url = resource
    file_path = get_path(file_name, dir_path)
    response = requests.get(full_url, stream=True)
    response.raise_for_status()
    write_response_to_file(file_path, full_url, response)


@logging_info('Writing response to file')
def write_response_to_file(file_path, url, response):
    total_size = CHUNK_SIZE
    if response.headers.get('Content-Length'):
        total_size = int(response.headers.get('Content-Length'))
    with open(file_path, 'wb') as file:
        with ChargingBar(url, max=total_size / CHUNK_SIZE) as bar:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)
                bar.next()
