import pytest
import tempfile
from page_loader.page_loader import download_images, create_download_dir
from os.path import split, join
import re
from tests.test_download import FORBIDDEN_CHARS
from pathlib import Path
import requests_mock
import requests
from shutil import copyfile
import filecmp

from bs4 import BeautifulSoup

URL = 'https://badcode.ru'
#HTML_NAME = 'images-fixture-before'
HTML_PATH_BEFORE = 'tests/fixtures/images_download_test/images-fixture-before.html'
HTML_PATH_AFTER = 'tests/fixtures/images_download_test/images-fixture-after.html'

netloc = 'badcode.ru'

IMAGE_1_PATH_BEFORE = 'tests/fixtures/images_download_test/badcode-2.png'
IMAGE_2_PATH_BEFORE = 'tests/fixtures/images_download_test/game-boy-color.jpg'
IMAGE_1_PATH_AFTER = 'images-fixture-before_files/badcode-ru-content-images-2020-01-badcode-2.png'
IMAGE_2_PATH_AFTER = 'images-fixture-before_files/badcode-ru-content-images-2018-11-game-boy-color.jpg'


def test_download_images_mock(requests_mock):
    requests_mock.get(URL, text='data')
    assert 'data' == requests.get(URL).text


def test_download_images_mocking(requests_mock):

    with tempfile.TemporaryDirectory() as tmp_directory:
        requests_mock.get(URL, content=open(HTML_PATH_BEFORE, 'rb').read())
        requests_mock.get(
            URL + '/content/images/2020/01/badcode-2.png',
            content=open(IMAGE_1_PATH_BEFORE, 'rb').read())
        requests_mock.get(
            URL + '/content/images/2018/11/game-boy-color.jpg',
            content=open(IMAGE_2_PATH_BEFORE, 'rb').read())
        copy_html_path = join(tmp_directory, split(HTML_PATH_BEFORE)[1])
        copyfile(HTML_PATH_BEFORE, copy_html_path)
        download_dir = create_download_dir(copy_html_path)
        download_images(copy_html_path, download_dir, URL, netloc)

        html_after = BeautifulSoup(open(HTML_PATH_AFTER, 'r'), 'html.parser')
        html_result = BeautifulSoup(open(copy_html_path, 'r'), 'html.parser')
        # find all "src" in both files
        image_links1 = html_after.find_all('img')
        image_links2 = html_result.find_all('img')
        src1 = []
        src2 = []
        for link in image_links1:
            src1.append(link['src'])
        for link in image_links2:
            src2.append(link['src'])
        assert src1 == src2
        assert filecmp.cmp(IMAGE_1_PATH_BEFORE, f'{tmp_directory}/{IMAGE_1_PATH_AFTER}', shallow=False)
        assert filecmp.cmp(IMAGE_2_PATH_BEFORE, f'{tmp_directory}/{IMAGE_2_PATH_AFTER}', shallow=False)


def test_download_images_exceptions():
    # TODO discuss with the mentor
    with tempfile.TemporaryDirectory() as tmp_directory:
        with pytest.raises(FileNotFoundError):
            download_images('', tmp_directory, URL, netloc)

    with pytest.raises(FileNotFoundError):
        download_images(HTML_PATH_BEFORE, '/undefined', URL, netloc)