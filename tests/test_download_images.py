import pytest
import tempfile
from page_loader.page_loader import download_images
from os.path import split, join
import re
from tests.test_download import FORBIDDEN_CHARS
from pathlib import Path
import requests_mock
import requests
from shutil import copyfile
import filecmp

URL = 'https://badcode.ru'
HTML_PATH = 'tests/fixtures/badcode-ru-docker-fixture.html'
# TODO this:
netloc = 'badcode.ru'


def test_download_images_mock(requests_mock):
    requests_mock.get(URL, text='data')
    assert 'data' == requests.get(URL).text


def test_download_images():
    with tempfile.TemporaryDirectory() as tmp_directory:
        copy_html_path = join(tmp_directory, split(HTML_PATH)[1])
        copyfile(HTML_PATH, copy_html_path)
        images_paths = download_images(copy_html_path, tmp_directory, URL, netloc)

        for image_path in images_paths:
            image = Path(image_path)
            image_name = split(image_path)[-1]
            assert isinstance(image_path, str)
            assert image.is_file()
            assert not re.search(FORBIDDEN_CHARS, image_name)
            assert not ('https---' in image_path)
        assert not filecmp.cmp(HTML_PATH, copy_html_path)  # TODO remake


def test_download_images_exceptions():
    # TODO discuss with the mentor
    with tempfile.TemporaryDirectory() as tmp_directory:
        with pytest.raises(FileNotFoundError):
            download_images('', tmp_directory, domain_name, netloc)

    with pytest.raises(FileNotFoundError):
        download_images(HTML_PATH, '/undefined', domain_name, netloc)