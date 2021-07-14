import requests
from urllib.parse import urlparse
import re
from pathlib import Path
from os.path import join


def get_file(url, file_path):
    response = requests.get(url, stream=True)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def download(url, output_path):
    directory = Path(output_path)
    if not directory.is_dir():
        raise FileNotFoundError
    parsed_url = urlparse(url)
    url_path = join(parsed_url.netloc, parsed_url.path)
    formatted_url_path = re.sub(r'[^0-9a-z-.]', '-', url_path)
    file_path = f'{output_path}/{formatted_url_path}{".html"}'
    get_file(url, file_path)

    return file_path
