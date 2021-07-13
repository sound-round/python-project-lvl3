import requests
from urllib.parse import urlparse
import re

def get_file(url, file_path):
    response = requests.get(url, stream=True)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def download(url, output_path):

    parsed_url = urlparse(url)
    url_path = f'{parsed_url.netloc}{parsed_url.path}'
    formatted_url_path = re.sub(r'[^0-9a-z-.]', '-', url_path)

    file_path = f'{output_path}/{formatted_url_path}{".html"}'
    get_file(url, file_path)

    return file_path
