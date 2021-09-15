from page_loader.logger import logging_info
from urllib.parse import urlparse, urljoin
from os.path import split
from page_loader.support_functions import write_file, get_path, get_full_name
import logging
import requests


TAGS_AND_ATTRIBUTES_PAIRS = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)


@logging_info('Getting input data')
def get_resources(file):
    resources = []
    for tag, attr in TAGS_AND_ATTRIBUTES_PAIRS:
        links = file.find_all(tag)
        resources.append((links, attr))
    return resources


def format_resource(url, resource, dir_path):
    links, attr = resource
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    for link in links:
        source = link.get(attr)
        if not source:
            continue
        if urlparse(source).netloc and urlparse(source).netloc != netloc:
            continue
        source = urlparse(source).path
        full_url = urljoin(url + '/', source)
        file_name = get_full_name(full_url)
        file_path = get_path(file_name, dir_path)
        logging.info('Requesting to %s', full_url)
        # TODO this:
        response = requests.get(full_url, stream=True) # TODO разделить на два цикла
        response.raise_for_status()
        write_file(file_path, full_url, response)

        dir_name = split(dir_path)[1]
        source_path = get_path(file_name, dir_name)
        link[attr] = source_path
