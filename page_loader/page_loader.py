import requests
from urllib.parse import urlparse
import re
from pathlib import Path
import os
from os.path import splitext


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

def download_images(html_path, dir_path):
    pass


def download(url, output_path=os.getcwd(), library=requests):
    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError
    parsed_url = urlparse(url)
    file_name = f'{parsed_url.netloc}{parsed_url.path}'
    formatted_file_name = re.sub(r'[^0-9a-zA-Z-]', '-', file_name).lower()
    file_path = f'{output_path}/{formatted_file_name}{".html"}'
    download_html(url, file_path, library)
    download_dir_path = create_download_dir(file_path)
    download_images(file_path, download_dir_path)
    return file_path
