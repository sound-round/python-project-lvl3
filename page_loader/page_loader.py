import requests
from urllib.parse import urlparse
import re
from pathlib import Path
import os
from os.path import splitext, join
from bs4 import BeautifulSoup


FORBIDDEN_CHARS = r'[^0-9a-zA-Z-]'


def download_html(url, file_path, client):
    response = client.get(url, stream=True)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def create_download_dir(html_path):
    root, _ = splitext(html_path)
    dir_path = root + '_files'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def download_images(html_path, dir_path, domain_name, netloc):
    html_file = open(html_path, 'r')
    parsed_html = BeautifulSoup(html_file, 'html.parser')
    image_links = parsed_html.find_all('img')
    for link in image_links:
        source = link.get('src')
        url = join(domain_name, source)
        image_name = join(netloc, source)
        formatted_image_name = re.sub(FORBIDDEN_CHARS, '-', image_name).lower()
        image_path = join(dir_path, formatted_image_name)

        response = requests.get(url, stream=True)

        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        # TODO change html.
        



def download(url, output_path=os.getcwd(), library=requests):
    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    html_name = f'{netloc}{parsed_url.path}'
    formatted_html_name = re.sub(FORBIDDEN_CHARS, '-', html_name).lower()
    html_path = f'{output_path}/{formatted_html_name}{".html"}'
    download_html(url, html_path, library)
    download_dir_path = create_download_dir(html_path)
    domain_name = join(parsed_url.scheme, parsed_url.netloc)
    download_images(html_path, download_dir_path, domain_name, netloc)

    return html_path
