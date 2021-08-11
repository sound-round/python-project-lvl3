import pytest
import tempfile
import os
import pathlib
from page_loader.page_loader import download_resources, download
from os.path import split, join
import requests
from shutil import copyfile
from page_loader.logger import configure_logging
import logging


configure_logging()


WRONG_URL = 'https://ru.HEXLET.io/courses'
URL = 'https://ru.hexlet.io'
NETLOC = 'ru.hexlet.io'
FIXTURES_PATH = 'fixtures'
HTML_NAME = 'ru-hexlet-io.html'
DOWNLOAD_DIR_NAME = 'ru-hexlet-io_files'
RESOURCES = [
    (
        '/courses',
        'courses.html',
        'ru-hexlet-io-courses.html'
    ),
    (
        '/assets/application.css',
        'application.css',
        'ru-hexlet-io-assets-application.css'
    ),
    (
        '/assets/professions/nodejs.png',
        'nodejs.png',
        'ru-hexlet-io-assets-professions-nodejs.png'
    ),
    (
        '/assets/professions/nodejs1.png',
        'nodejs1.png',
        'ru-hexlet-io-assets-professions-nodejs1.png'
    ),
    (
        '/assets/professions/nodejs2.png',
        'nodejs2.png',
        'ru-hexlet-io-assets-professions-nodejs2.png'
    ),
    (
        '/packs/js/runtime.js',
        'runtime.js',
        'ru-hexlet-io-packs-js-runtime.js'
    ),
]


def read(file_path, mode='r'):
    with open(file_path, mode) as f:
        file = f.read()
    return file


def get_fixture_path(fixture_name):
    return os.path.join(
        pathlib.Path(__file__).absolute().parent,
        FIXTURES_PATH,
        fixture_name
    )


def test_download(requests_mock):
    with tempfile.TemporaryDirectory() as tmp_directory:
        logging.info(f'tmp_dir_name: {tmp_directory}')
        requests_mock.get(
            URL,
            content=read(get_fixture_path(HTML_NAME), 'rb'),
            status_code=200,
        )
        for items in RESOURCES:
            subpath, fixture_name, loaded_file_name = items
            fixture_path = get_fixture_path(fixture_name)
            requests_mock.get(
                URL + subpath,
                content=read(fixture_path, 'rb'),
                status_code=200,
            )
        download(URL, tmp_directory)

        assert read(
            get_fixture_path(f'after/{HTML_NAME}')
        ) == read(
            f'{tmp_directory}/{HTML_NAME}'
        )

        for items in RESOURCES:
            subpath, fixture_name, loaded_file_name = items
            fixture_path = get_fixture_path(fixture_name)
            assert read(
                fixture_path, 'rb',
            ) == read(
                f'{tmp_directory}/{DOWNLOAD_DIR_NAME}/{loaded_file_name}', 'rb',
            )


def test_download_exceptions(requests_mock):
    requests_mock.get(
        'http://www.test.com/',
        status_code=404,
    )

    with tempfile.TemporaryDirectory() as tmp_directory:

        with pytest.raises(ValueError):
            download('', tmp_directory)

        with pytest.raises(requests.exceptions.HTTPError) as e:
            download('http://www.test.com/', tmp_directory)
        assert str(e.value) == '404 Client Error: ' \
                               'None for url: http://www.test.com/'

    with pytest.raises(FileNotFoundError):
        download(WRONG_URL, '/undefined')