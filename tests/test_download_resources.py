import pytest
import tempfile
import os
import pathlib
from page_loader.page_loader import download_resources, create_download_dir
from os.path import split, join
import requests
from shutil import copyfile
import filecmp

from bs4 import BeautifulSoup


URL = 'https://ru.hexlet.io'
NETLOC = 'ru.hexlet.io'
FIXTURES_PATH = 'fixtures/resources_download_test'
HTML = 'ru-hexlet-io-courses.html'
DATA = [
    ('/assets/application.css', 'application.css', 'ru-hexlet-io-assets-application.css'),
    ('/courses', 'courses', 'ru-hexlet-io-courses.html'),
    ('/assets/professions/nodejs.png', 'nodejs.png', 'ru-hexlet-io-assets-professions-nodejs.png'),
    ('/packs/js/runtime.js', 'runtime.js', 'ru-hexlet-io-packs-js-runtime.js'),
]

'''
HTML_PATH_AFTER = (
    'tests/fixtures/images_download_test/images-fixture-after.html'
)'''


def read_in_bytes(file_path):
    with open(file_path, 'rb') as f:
        file = f.read()
    return file


def get_fixture_path(fixture_name):
    return os.path.join(
        pathlib.Path(__file__).absolute().parent,
        FIXTURES_PATH,
        fixture_name
    )


def test_download_images_mock(requests_mock):
    requests_mock.get(URL, text='data')
    assert 'data' == requests.get(URL).text


def test_resources_download_mocking(requests_mock):
    with tempfile.TemporaryDirectory() as tmp_directory:
        #requests_mock.get(URL, content=read_in_bytes(HTML_PATH_BEFORE))
        for items in DATA:
            subpath, fixture, loaded_file = items
            fixture_path = get_fixture_path(fixture)
            requests_mock.get(
                URL + subpath,
                content=read_in_bytes(fixture_path))
        html_path = get_fixture_path(HTML)
        copy_html_path = join(tmp_directory, split(html_path)[1])
        copyfile(html_path, copy_html_path)
        download_dir = create_download_dir(copy_html_path)
        download_resources(copy_html_path, download_dir, URL, NETLOC)

        #html_after = BeautifulSoup(open(HTML_PATH_AFTER, 'r'), 'html.parser')
        #html_result = BeautifulSoup(open(copy_html_path, 'r'), 'html.parser')
        # find all "src" in both files
        #image_links1 = html_after.find_all('img')
        #image_links2 = html_result.find_all('img')
        #src1 = []
        #src2 = []
        #for link in image_links1:
        #    src1.append(link['src'])
        #for link in image_links2:
        #    src2.append(link['src'])

        #assert src1 == src2
        for items in DATA:
            subpath, fixture, loaded_file = items
            fixture_path = get_fixture_path(fixture)
            assert filecmp.cmp(
                fixture_path,
                f'{tmp_directory}/ru-hexlet-io-courses_files/{loaded_file}',
                shallow=False
            )
        assert filecmp.cmp(
                get_fixture_path('after/ru-hexlet-io-courses.html'),
                f'{tmp_directory}/ru-hexlet-io-courses.html',
                shallow=False
            )


def test_download_images_exceptions():
    # TODO discuss with the mentor
    with tempfile.TemporaryDirectory() as tmp_directory:
        with pytest.raises(FileNotFoundError):
            download_resources('', tmp_directory, URL, NETLOC)

    with pytest.raises(FileNotFoundError):
        html_path = get_fixture_path(HTML)
        download_resources(html_path, '/undefined', URL, NETLOC)
