from page_loader.logger import logging_info
from urllib.parse import urlparse, urljoin
from os.path import split, splitext, join
from page_loader.common import download_file, format_name
import logging
import requests


TAGS_AND_ATTRIBUTES = (
    ('img', 'src'), ('link', 'href'), ('script', 'src'),
)
HTML_EXT = '.html'


def get_path(url, output_path):
    parsed_url = urlparse(url)
    file_name, file_ext = splitext(f'{parsed_url.netloc}{parsed_url.path}')
    if not file_ext:
        file_ext = HTML_EXT
    formatted_file_name = format_name(file_name)
    return join(output_path, formatted_file_name) + file_ext


@logging_info('Getting input data')
def get_resources_data(file):

    # get pairs of links(list) and tag
    resources_data = []
    for tag, attr in TAGS_AND_ATTRIBUTES:
        links = file.find_all(tag)
        resources_data.append((links, attr))
    return resources_data


def download_resource(url, resource_data, dir_path):
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
        download_file(file_path, url, response)

        dir_name = split(dir_path)[1]
        source_path = get_path(url, dir_name)
        link[attr] = source_path
